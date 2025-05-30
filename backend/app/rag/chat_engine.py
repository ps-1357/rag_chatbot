from typing import List, Dict, Any
import os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

class ChatEngine:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0.7
        )
        self.output_parser = StrOutputParser()
        self._setup_chain()

    def _setup_chain(self):
        template = """You are an expert insurance advisor helping users understand their insurance plans.
        Use the following context to answer the question. If you don't know the answer, say so.
        
        Context: {context}
        Question: {question}
        
        Answer in a clear and professional manner."""

        prompt = ChatPromptTemplate.from_template(template)
        
        self.chain = (
            {"context": self.vector_store.as_retriever(search_type="mmr"), "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | self.output_parser
        )

    def chat(self, message: str) -> Dict[str, str]:
        try:
            response = self.chain.invoke(message)
            docs = self.vector_store.similarity_search(message, k=2)
            sources = [doc.metadata.get("source", "") for doc in docs]
            return {
                "response": response,
                "sources": sources
            }
        except Exception as e:
            raise Exception(f"Error processing chat: {str(e)}")

    def _is_recommendation_query(self, message: str) -> bool:
        recommendation_keywords = [
            'best plan', 'best package', 'recommend', 'suggestion', 'which plan',
            'which package', 'suitable', 'good for me', 'right for me'
        ]
        return any(keyword in message.lower() for keyword in recommendation_keywords)

    def chat(self, message: str) -> Dict[str, Any]:
        try:
            if self._is_recommendation_query(message):
                enhanced_message = f"""
                Considering the user's query: '{message}'
                Compare the following aspects across all available plans:
                - Monthly premiums and deductibles
                - Coverage for specific needs mentioned
                - Out-of-pocket maximums
                - Network coverage
                - Special benefits or limitations
                """
                search_message = enhanced_message
            elif "2500 Gold" in message or "gold" in message.lower():
                search_message = message + " Americas Choice 2500 Gold plan SOB"
            else:
                search_message = message
                
            response = self.chain.invoke(search_message)
            
            docs = self.vector_store.similarity_search(search_message, k=2)
            sources_with_pages = [f"{doc.metadata.get('source', 'Unknown')} (Page {doc.metadata.get('page_label', '')})" for doc in docs if doc.metadata.get('source', 'Unknown') != 'Unknown']
            sources = [source for source in sources_with_pages if source != 'Unknown']
            
            if self._is_recommendation_query(message):
                response += "\n\nNote: This recommendation is based on the information provided. For the most accurate advice, consider consulting with an insurance advisor who can take into account your complete medical history and specific needs."
            
            return {
                "response": response,
                "sources": sources
            }
        except Exception as e:
            print(f"Error in chat processing: {str(e)}")
            raise 