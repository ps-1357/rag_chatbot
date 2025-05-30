import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

def load_documents(docs_dir: str) -> List:
    documents = []
    
    # Process each file in the docs directory
    for filename in os.listdir(docs_dir):
        file_path = os.path.join(docs_dir, filename)
        
        try:
            if filename.endswith('.pdf'):
                # Load PDF with better handling
                loader = PyPDFLoader(file_path)
                documents.extend(loader.load())
                print(f"Loaded PDF: {filename}")
                
            elif filename.endswith('.docx'):
                # Load DOCX files
                loader = Docx2txtLoader(file_path)
                documents.extend(loader.load())
                print(f"Loaded DOCX: {filename}")
                
        except Exception as e:
            print(f"Error loading {filename}: {str(e)}")
    
    return documents

def main():
    # Get the absolute path to the docs directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    docs_dir = os.path.join(current_dir, "docs")
    db_dir = os.path.join(current_dir, "vectorstore")
    
    print("Loading documents...")
    documents = load_documents(docs_dir)
    
    print("\nSplitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    splits = text_splitter.split_documents(documents)
    print(f"Created {len(splits)} text chunks")
    
    print("\nCreating vector store...")
    # Remove existing vector store if it exists
    if os.path.exists(db_dir):
        print("Removing existing vector store...")
        import shutil
        shutil.rmtree(db_dir)
    
    # Create new vector store
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=OpenAIEmbeddings(),
        persist_directory=db_dir
    )
    
    print(f"\nVector store created successfully with {len(splits)} chunks")
    print(f"Vector store location: {db_dir}")

if __name__ == "__main__":
    main() 