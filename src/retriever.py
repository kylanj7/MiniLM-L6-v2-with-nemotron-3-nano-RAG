"""
RAG retriever: combines vector search with LLM generation
"""
from langchain_community.llms import VLLM
from src.vector_store import VectorStoreManager
from config.settings import (
    LLM_MODEL, TOP_K_RESULTS, MAX_TOKENS, 
    TEMPERATURE
)


class RAGRetriever:
    """Main RAG pipeline for question answering"""
    
    def __init__(self):
        self.vs_manager = VectorStoreManager()
        self.vs_manager.create_or_load()
        
        self.llm = VLLM(model=LLM_MODEL, 
            trust_remote_code=True, 
            max_new_tokens=MAX_TOKENS, 
            temperature=TEMPERATURE, 
            tensor_parallel_size=2
        )
        
        print(f"✓ RAG Retriever initialized with {LLM_MODEL}")
    
    def retrieve_and_generate(self, query):
        """
        RAG pipeline: retrieve context and generate answer.
        
        Args:
            query: User question
            
        Returns:
            Dict with 'answer' and 'sources'
        """
        print(f"\n Query: {query}")
        
        # Retrieve relevant chunks
        docs = self.vs_manager.similarity_search(query, k=TOP_K_RESULTS)
        
        if not docs:
            return {
                "answer": "No relevant documents found in the knowledge base.",
                "sources": []
            }
        
        print(f"  Retrieved {len(docs)} relevant chunks")
        
        # Build context from retrieved chunks
        context = "\n\n".join([
            f"[Source: {doc.metadata.get('source_file', 'unknown')}]\n{doc.page_content}"
            for doc in docs
        ])
        
        # Construct prompt
        prompt = f"""Use the following context to answer the question. Be concise and accurate. If you cannot answer based on the context provided, say so clearly.

Context:
{context}

Question: {query}

Answer:"""
        
        # Generate response
        print("  Generating answer...")
        response = self.llm.invoke(prompt)
        
        sources = list(set([doc.metadata.get('source_file', 'unknown') for doc in docs]))
        
        return {
            "answer": response.strip(),
            "sources": sources
        }


if __name__ == "__main__":
    # Test retriever
    rag = RAGRetriever()
    
    test_query = "What is this document about?"
    result = rag.retrieve_and_generate(test_query)
    
    print(f"\n Answer:\n{result['answer']}")
    print(f"\n Sources: {', '.join(result['sources'])}")
