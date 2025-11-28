"""
Configuration settings for Lightweight RAG System
"""
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data" / "pdfs"
VECTOR_STORE_DIR = BASE_DIR / "vectorstore" / "chroma_db"

# Ensure directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)

# Chunking settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Ollama models
EMBEDDING_MODEL = "embeddinggemma:latest"
LLM_MODEL = "tinyllama:1.1b"
OLLAMA_BASE_URL = "http://localhost:11434"

# Vector store settings
COLLECTION_NAME = "enterprise_docs"
TOP_K_RESULTS = 3

# LLM generation settings
MAX_TOKENS = 2048
TEMPERATURE = 0.49

# Logging
LOG_LEVEL = "INFO"
