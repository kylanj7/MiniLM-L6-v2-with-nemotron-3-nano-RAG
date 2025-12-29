"""
Configuration settings for Huggingface RAG System
"""

import os
from pathlib import Path

# GPU Settings
NUMBER_OF_GPUs = 2
MEMORY_UTILIZATION = 0.9

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

# HuggingFace Models
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "nemotron-3-nano:latest"
OLLAMA_BASE_URL = "http://127.0.0.1:11434"

# Vector store settings
COLLECTION_NAME = "enterprise_docs"
TOP_K_RESULTS = 1

# LLM generation settings
MAX_MODEL_LENGTH = 8192
MAX_TOKENS = 2048
TEMPERATURE = 0.7

# Misc Settings
ENFORCE_EAGER = True

# Logging
LOG_LEVEL = "INFO"
