"""
Ollama embeddings interface for semantic search
"""
from langchain_ollama import OllamaEmbeddings
from config.settings import EMBEDDING_MODEL, OLLAMA_BASE_URL


def get_embeddings():
    """
    Initialize Ollama embeddings with Gemma model.
    
    Returns:
        OllamaEmbeddings: Configured embedding function
    """
    return OllamaEmbeddings(
        model=EMBEDDING_MODEL,
        base_url=OLLAMA_BASE_URL
    )


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
