# Huggingface RAG System with vLLM

Retrieval-Augmented Generation (RAG) system for enterprise document question-answering. Built with ChromaDB, vLLM, and HuggingFace embeddings for efficient local deployment.

## Features

- **Parallel PDF Processing**: Multi-core PDF extraction and chunking with PyMuPDF
- **Incremental Indexing**: Smart file tracking to avoid re-indexing unchanged documents
- **Local Inference**: Uses vLLM for fast local LLM inference with tensor parallelism
- **Semantic Search**: ChromaDB vector store with MiniLM embeddings
- **Modular Architecture**: Clean separation of concerns across chunking, embedding, storage, and retrieval

## System Architecture

```
┌─────────────┐
│   PDFs      │
│  (data/)    │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  pdf_chunker    │  ← Parallel extraction & chunking
│  (PyMuPDF)      │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  embeddings     │  ← HuggingFace MiniLM-L6-v2
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  vector_store   │  ← ChromaDB + incremental indexing
│  (Chroma)       │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│   retriever     │  ← vLLM (Phi-3.5-mini) + RAG pipeline
└─────────────────┘
```

## Prerequisites

- Python 3.10
- CUDA-capable GPU (recommended for vLLM)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/kylanj7/Huggingface-vLLM-RAG
cd Huggingface-vLLM-RAG
```

2. Create Virtual Environment 
```bash
conda create -n myrag python=3.10
conda activate myrag
pip install -r requirements.txt
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Verify installation:
```bash
python src/embeddings.py  # Test embeddings
```

## Quick Start

### 1. Add Your Documents

Place PDF files in the `data/pdfs/` directory:
```bash
mkdir -p data/pdfs
cp your-documents/*.pdf data/pdfs/
```

### 2. Index Documents

Index your documents into the vector database:
```bash
# Index new or modified PDFs only (recommended)
python3 main.py index

# Force re-index all PDFs (slower, use if needed)
python3 main.py index --force
```

This will:
- Extract text from all PDFs in parallel
- Chunk documents into 1000-character segments (200 char overlap)
- Generate embeddings and store in ChromaDB

### 3. Query the System

## Querying the System

Start an interactive query session:
```bash
python3 main.py query
```

## Configuration

Edit `config/settings.py` to customize:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `CHUNK_SIZE` | 1000 | Characters per document chunk |
| `CHUNK_OVERLAP` | 200 | Overlap between chunks |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | HuggingFace embedding model |
| `LLM_MODEL` | `Phi-3.5-mini-instruct` | vLLM generation model |
| `TOP_K_RESULTS` | 3 | Number of chunks to retrieve |
| `MAX_TOKENS` | 2048 | Maximum generation length |
| `TEMPERATURE` | 0.49 | LLM sampling temperature |

## Module Overview

### `src/pdf_chunker.py`
- Parallel PDF text extraction using PyMuPDF
- Multi-core processing with `ProcessPoolExecutor`
- Recursive character-based text splitting
- Metadata tracking for source attribution

### `src/embeddings.py`
- HuggingFace `sentence-transformers` integration
- Configurable embedding model selection
- Standalone testing capability

### `src/vector_store.py`
- ChromaDB persistence management
- File hash-based change detection
- Incremental indexing with `indexed_files.json` log
- Batch document insertion with progress tracking

### `src/retriever.py`
- vLLM-powered generation with tensor parallelism
- Context-aware prompt construction
- Semantic similarity search
- Source citation tracking

## Performance Considerations

### GPU Memory
vLLM uses tensor parallelism (`tensor_parallel_size=2`) for multi-GPU setups. Adjust based on your hardware:
```python
# In retriever.py
self.llm = VLLM(
    model=LLM_MODEL,
    tensor_parallel_size=1,  # Use 1 for single GPU
    ...
)
```

### Batch Processing
Vector store indexing uses batches of 100 chunks. Increase for faster indexing on high-memory systems:
```python
vs_manager.add_documents(chunks, batch_size=500)
```

### CPU Cores
PDF processing uses all available CPU cores by default. Limit if needed:
```python
# In pdf_chunker.py
max_workers = 4  # Instead of multiprocessing.cpu_count()
```

## Incremental Updates

The system automatically tracks indexed files. To add new documents:

1. Add PDFs to `data/pdfs/`
2. Re-run chunker - only new/modified files will be processed
3. New chunks are appended to existing vector store

To force re-indexing:
```python
vs_manager = VectorStoreManager()
vs_manager.delete_collection()  # Clears everything
```

## Troubleshooting

### vLLM Import Errors
```bash
# Ensure CUDA is available
python -c "import torch; print(torch.cuda.is_available())"

# Reinstall vLLM with CUDA support
pip install vllm --extra-index-url https://download.pytorch.org/whl/cu118
```

### Out of Memory
Reduce batch size or use smaller models:
```python
# Smaller embedding model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L12-v2"

# Smaller LLM
LLM_MODEL = "microsoft/phi-2"
```

### ChromaDB Persistence Issues
```bash
# Clear and rebuild
rm -rf vectorstore/chroma_db
python src/pdf_chunker.py
```

## Project Structure

```
.
├── config/
│   └── settings.py          # Configuration parameters
├── data/
│   └── pdfs/                # Input PDF directory
├── src/
│   ├── pdf_chunker.py       # PDF processing
│   ├── embeddings.py        # Embedding interface
│   ├── vector_store.py      # ChromaDB management
│   └── retriever.py         # RAG pipeline
├── vectorstore/
│   └── chroma_db/           # Persisted vector database
├── requirements.txt
└── README.md
```

## Dependencies

Core libraries:
- `langchain` - RAG framework
- `langchain-chroma` - ChromaDB integration
- `langchain-huggingface` - HuggingFace embeddings
- `vllm` - Fast LLM inference engine
- `PyMuPDF` - PDF text extraction
- `chromadb` - Vector database
- `sentence-transformers` - Embedding models

## License

MIT License

## Contributing

Contributions welcome! Please submit pull requests or open issues for bugs and feature requests.

## Acknowledgments

- Built with [vLLM](https://github.com/vllm-project/vllm) for efficient inference
- Powered by [ChromaDB](https://www.trychroma.com/) vector database
- Uses HuggingFace [sentence-transformers](https://www.sbert.net/)
