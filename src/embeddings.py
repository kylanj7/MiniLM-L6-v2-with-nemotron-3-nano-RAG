"""
Ollama embeddings interface for semantic search
"""
from langchain_huggingface import HuggingFaceEmbeddings
from config.settings import EMBEDDING_MODEL


def get_embeddings():
    """
    Initialize Ollama embeddings with Gemma model.
    
    Returns:
        OllamaEmbeddings: Configured embedding function
    """
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    


if __name__ == "__main__":
    # Test embeddings
    embeddings = get_embeddings()
    test_text = "This is a test document for enterprise RAG system."
    
    try:
        result = embeddings.embed_query(test_text)
        print(f"✓ Embeddings working! Vector dimension: {len(result)}")
    except Exception as e:
        print(f"✗ Embeddings test failed: {e}")
        print("  Make sure Ollama is running and gemma:2b is pulled.")
