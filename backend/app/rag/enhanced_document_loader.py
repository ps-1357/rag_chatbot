from typing import List, Optional
import os
import camelot
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document
import pandas as pd

class EnhancedDocumentLoader:
    def __init__(self, docs_dir: str, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.docs_dir = docs_dir
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )
    
    def _try_extract_tables(self, file_path: str, flavor: str) -> List[Document]:
        """Try to extract tables with a specific flavor."""
        try:
            kwargs = {
                'pages': 'all',
                'flavor': flavor,
                'suppress_stdout': True
            }
            
            # Add specific settings for stream flavor
            if flavor == 'stream':
                kwargs.update({
                    'edge_tol': 500,  # More tolerant of table edges
                    'row_tol': 10,    # More tolerant of row alignment
                })
            
            tables = camelot.read_pdf(file_path, **kwargs)
            
            documents = []
            if len(tables) > 0:
                print(f"Found {len(tables)} potential tables using {flavor} flavor in {os.path.basename(file_path)}")
                
                for i, table in enumerate(tables):
                    # For stream flavor, we're more lenient with accuracy
                    min_accuracy = 60 if flavor == 'stream' else 80
                    if table.parsing_report['accuracy'] > min_accuracy:
                        # Convert table to markdown format
                        df = table.df
                        # Clean up the table data
                        df = df.replace('', pd.NA).dropna(how='all').fillna('')
                        markdown_table = df.to_markdown(index=False)
                        
                        doc = Document(
                            page_content=f"Table {i+1}:\n{markdown_table}",
                            metadata={
                                "source": os.path.basename(file_path),
                                "page": table.page,
                                "type": "table",
                                "table_number": i + 1,
                                "accuracy": table.parsing_report['accuracy'],
                                "extraction_method": flavor
                            }
                        )
                        documents.append(doc)
            
            return documents
        except Exception as e:
            print(f"Warning: Error extracting tables with {flavor} flavor from {os.path.basename(file_path)}: {str(e)}")
            return []
    
    def _extract_tables_from_pdf(self, file_path: str) -> List[Document]:
        """Extract tables from PDF using multiple methods."""
        # Try stream first as it doesn't require Ghostscript
        documents = self._try_extract_tables(file_path, 'stream')
        
        # If stream didn't find any tables, try lattice
        if not documents:
            lattice_docs = self._try_extract_tables(file_path, 'lattice')
            documents.extend(lattice_docs)
        
        return documents
    
    def _extract_text_from_pdf(self, file_path: str) -> List[Document]:
        """Extract regular text from PDF using PyPDFLoader."""
        loader = PyPDFLoader(file_path)
        return loader.load()
    
    def load_documents(self) -> List[Document]:
        """Load all supported documents with enhanced PDF processing."""
        documents = []
        
        for file in os.listdir(self.docs_dir):
            file_path = os.path.join(self.docs_dir, file)
            
            if file.endswith('.pdf'):
                # Extract tables first
                table_docs = self._extract_tables_from_pdf(file_path)
                if table_docs:
                    print(f"Successfully extracted {len(table_docs)} tables from {file}")
                documents.extend(table_docs)
                
                # Extract regular text
                text_docs = self._extract_text_from_pdf(file_path)
                # Mark these as non-table content
                for doc in text_docs:
                    doc.metadata["type"] = "text"
                documents.extend(text_docs)
                
            elif file.endswith('.docx') or file.endswith('.doc'):
                loader = Docx2txtLoader(file_path)
                docs = loader.load()
                for doc in docs:
                    doc.metadata["type"] = "text"
                documents.extend(docs)
        
        return documents
    
    def create_vector_store(self, persist_directory: Optional[str] = None) -> Chroma:
        """Create and optionally persist a vector store from the documents."""
        documents = self.load_documents()
        texts = self.text_splitter.split_documents(documents)
        
        # Initialize vector store
        embeddings = OpenAIEmbeddings()
        
        if persist_directory:
            vector_store = Chroma.from_documents(
                documents=texts,
                embedding=embeddings,
                persist_directory=persist_directory
            )
        else:
            vector_store = Chroma.from_documents(
                documents=texts,
                embedding=embeddings
            )
        
        return vector_store 