# Lightweight Enterprise RAG
A lightweight Retrieval-Augmented Generation (RAG) system designed for enterprise executives and employees who require confidential AI assistance for productivity tasks while maintaining strict data confidentiality.

## Overview

This system leverages **TinyLlama 1.1b** as the language model and **Embedded Gemma 300m** for embeddings to deliver intelligent document retrieval and question-answering capabilities on consumer-grade hardware.

## Key Features

- **Enterprise-Grade Security**: All data processing occurs locally—no external API calls or data transmission
- **Executive-Ready**: Optimized for business documents, reports, and confidential materials
- **Lightweight Performance**: Runs efficiently on modern mid-tier mobile processors (16GB+ RAM recommended)
- **Travel-Friendly**: Fully functional offline—perfect for flights, remote locations, and secure facilities
- **Fast Setup**: Powered by Ollama API for streamlined deployment and rapid local inference
- **Intelligent Retrieval**: Multiprocessing-enabled PDF chunking with semantic search capabilities
- **Confidential RAG**: Private document indexing with persistent vector storage using ChromaDB
- **Incremental Indexing**: Only processes new or modified documents, saving time on updates
- **Scalable**: Larger models can scale with the system's resources

## System Requirements

### Minimal Requirments
- **Processor**: Modern dual-core CPU (Intel i5 11th gen or Ryzen zen3 or higher)
- **RAM**: >16GB (32GB recommended for larger document collections)
- **Storage**: 256GB free space (Only 2GB for models + extra for documents/vector store)
- **OS**: Windows 10/11, macOS 12+, or Linux (Ubuntu 20.04+)

### Minimum Software 
- Python 3.10 or higher
- Ollama runtime environment

---

## For Automatic Tnstallation Follow the Steps Below

 - This method automatically updates your system(Linux), installs pthon3.10-env & activates the rag_env, installs curl(Linux), ollama, and pulls the Tinyllama1.1b & GemmaEmbed300m models. 

### Step 1: Clone the Repository
```bash
git clone https://github.com/kylanj7/Lightweight-Enterprise-RAG
```
## Change Directories
```
cd Lightweight-Enterprise-RAG
```
## Make the Script Executable
```
chmod +x install.sh
```
## Run the Bash Script
```
source install.sh # Run as source to activate the venv
```
## Automatic Deployment
 - This method automatically updates your system, installs project dependencies (requirements.txt), installs pthon3.10-env & activates the rag_env, installs curl, ollama, and pulls the Tinyllama1.1b & GemmaEmbed300m models. 

## For Automatic Windows Installation

### Install Git
```bash
winget install --id Git.Git -e --source winget
```
### Clone the Repository
```bash
git clone https://github.com/kylanj7/Lightweight-Enterprise-RAG
```
## Change Directories
```
cd Lightweight-Enterprise-RAG
```
## Run the PowerShell Script
```
./install.ps1
```
 - This method installs Ollama, updates the path, installs pip, installs project dependencies (requirements.txt), activates the Virtual Environment and pulls TinLlama1.1b & GemmaEmbedding300m models.

# Follow the Steps Below for Manual Set-up

### Step 1: Clone the Repository
```bash
git clone https://github.com/kylanj7/Lightweight-Enterprise-RAG.git
```
## Change Directories
```
cd Lightweight-Enterprise-RAG
```

### Step 2: Set Up Python Virtual Environment
```bash
# Create virtual environment
python3 -m venv rag_venv
```
```
# Activate virtual environment
# On Linux/macOS:
source rag_venv/bin/activate
```
```
# On Windows:
rag_venv\Scripts\activate
```

### Step 3: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Install Ollama

Visit [https://ollama.ai](https://ollama.ai) and download Ollama for your operating system.

**Installation commands:**
```bash
# Linux
curl -fsSL https://ollama.ai/install.sh | sh
```
```
# macOS
brew install ollama
```
```
# Windows
winget install --id Git.Git -e --source winget
```

### Step 5: Start Ollama Service
```bash
# Start Ollama server (run in a separate terminal)
ollama serve
```

Verify Ollama is running:
```bash
curl http://localhost:11434/api/tags
```

### Step 6: Pull Required AI Models
```bash
# Pull the LLM model (TinyLlama 1.1b - ~637MB)
ollama pull tinyllama:1.1b

# Pull the embedding model (embeddinggemma:latest - ~300MB)
ollama pull embeddinggemma:latest

# Verify models are installed
ollama list
```

Expected output:
```
NAME                    ID              SIZE      MODIFIED
tinyllama:1.1b          xyz123...       637 MB    2 minutes ago
embeddinggemma:latest   abc456...       274 MB    1 minute ago
```

---

# Usage Guide

### Adding Documents

1. Place your PDF files in the `data/pdfs/` directory:
```bash
cp /path/to/your/documents/*.pdf data/pdfs/
```

2. Supported file types:
   - PDF documents (text-based, not scanned images)
   - Multiple PDFs can be added at once

### Indexing Documents

Index your documents into the vector database:
```bash
# Index new or modified PDFs only (recommended)
python3 main.py index

# Force re-index all PDFs (slower, use if needed)
python3 main.py index --force
```

**What happens during indexing:**
- PDFs are processed in parallel using all CPU cores
- Text is extracted and split into semantic chunks
- Chunks are embedded using the Gemma Embedded model
- Embeddings are stored in ChromaDB for fast retrieval
- Progress is displayed in real-time

**Expected output:**
```
============================================================
INDEXING DOCUMENTS
============================================================
Processing 9 new/changed file(s):

Processing: comptia-cloud-cv0-003-exam-objectives-5-0.pdf
Adding 44 chunks in batches of 100...
  Processing batch 1/1
Added 44 chunks successfully
  Added 44 chunks from comptia-cloud-cv0-003-exam-objectives-5-0.pdf

...

Indexing complete!
  New chunks added: 4319
  Total chunks in database: 4319
  Indexed files: 9
```

### Querying the System

Start an interactive query session:
```bash
python3 main.py query
```

**Example session:**
```
============================================================
RAG QUERY SYSTEM
============================================================
Type 'exit' or 'quit' to stop

Your question: What are the CompTIA Cloud+ exam objectives?

Query: What are the CompTIA Cloud+ exam objectives?
  Retrieved 3 relevant chunks
  Generating answer...

Answer:
The CompTIA Cloud+ exam objectives cover four main domains: 
1. Cloud architecture and design
2. Deployment of cloud services and solutions
3. Maintenance, security, and optimization of cloud environments
4. Troubleshooting common cloud management issues

Sources: comptia-cloud-cv0-003-exam-objectives-5-0.pdf
------------------------------------------------------------

Your question: How do neural networks learn?

Query: How do neural networks learn?
  Retrieved 3 relevant chunks
  Generating answer...

Answer:
Neural networks learn through a process called backpropagation...

Sources: Neural-Networks-from-Scratch-in-Python.pdf
------------------------------------------------------------

Your question: exit

Goodbye!
```

### Checking Database Statistics

View information about your indexed documents:
```bash
python3 main.py stats
```

**Output:**
```
Vector Store Statistics
  Collection: enterprise_docs
  Total chunks: 4319
  Indexed files: 9

Indexed Files:
  1. 913-comptia-network-deluxe-study-guide.pdf
  2. PyTorch-Ebook.pdf
  3. cloud-data-engineering-for-dummies.pdf
  ...
```

### Resetting the Database

To clear all indexed documents and start fresh:
```bash
python3 main.py reset
```

You will be prompted for confirmation:
```
WARNING: Are you sure you want to delete all indexed documents? (yes/no): yes
Deleted collection: enterprise_docs
Cleared index log
Database reset complete
```

---

## Project Structure
```
lightweight-rag-enterprise/
│
├── config/
│   ├── __init__.py
│   └── settings.py              # Configuration settings
│
├── data/
│   └── pdfs/                    # Place your PDF documents here
│
├── vectorstore/
│   └── chroma_db/               # ChromaDB storage (auto-generated)
│
├── src/
│   ├── __init__.py
│   ├── pdf_chunker.py           # PDF processing and chunking
│   ├── embeddings.py            # Ollama embedding interface
│   ├── vector_store.py          # ChromaDB management
│   └── retriever.py             # RAG query logic
│
├── main.py                      # Main CLI interface
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── .gitignore                   # Git ignore rules
```

---

## Configuration

Edit `config/settings.py` to customize behavior:
```python
# Chunking settings
CHUNK_SIZE = 1000              # Characters per chunk
CHUNK_OVERLAP = 200            # Overlap between chunks

# Ollama models
EMBEDDING_MODEL = "embeddinggemma:latest"
LLM_MODEL = "tinyllama:1.1b"
OLLAMA_BASE_URL = "http://localhost:11434"

# Vector store settings
TOP_K_RESULTS = 3              # Number of chunks to retrieve per query

# LLM generation settings
MAX_TOKENS = 512               # Maximum response length
TEMPERATURE = 0.7              # Creativity (0.0-1.0)
```

---

## Performance Benchmarks

- **Initial Indexing**: 50-100 pages/minute (varies by CPU)
- **Query Latency**: Less than 3 seconds for typical queries
- **Memory Footprint**: 2-4GB during active use
- **Disk Usage**: Approximately 500MB per 1,000 document pages (vector store)

---

## Troubleshooting

### Ollama Connection Issues

**Problem:** `Connection refused to localhost:11434`

**Solution:**
```bash
# Ensure Ollama is running
ollama serve

# Check if it's accessible
curl http://localhost:11434/api/tags
```

### Model Not Found

**Problem:** `model "tinyllama:1.1b" not found`

**Solution:**
```bash
# Pull the missing model
ollama pull tinyllama:1.1b
ollama pull embeddinggemma:latest

# Verify installation
ollama list
```

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'langchain'`

**Solution:**
```bash
# Ensure virtual environment is activated
source rag_venv/bin/activate  # Linux/macOS
# or
rag_venv\Scripts\activate      # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### No Text Extracted from PDFs

**Problem:** PDFs indexed but queries return no results

**Solution:**
- Ensure PDFs contain actual text (not scanned images)
- For scanned PDFs, use OCR preprocessing before indexing
- Check `chunks_output.txt` to verify text extraction quality

### Slow Indexing Performance

**Problem:** Indexing takes hours for large document sets

**Solution:**
- First-time indexing is slower; subsequent updates are incremental
- Ensure Ollama is using GPU if available (check with `nvidia-smi`)
- Consider indexing in smaller batches
- Adjust `batch_size` in `vector_store.py` (default: 100)

---

## Security and Privacy

- **Zero external network calls**: All processing is local
- **No telemetry or tracking**: Your data never leaves your device
- **Encrypted storage compatible**: Works with disk encryption
- **Air-gap deployable**: No internet required post-setup
- **GDPR/HIPAA friendly**: Data never leaves the device

### Best Practices

1. **Sensitive Documents**: Keep `data/pdfs/` and `vectorstore/` outside version control
2. **Access Control**: Restrict file system permissions appropriately
3. **Data Retention**: Regularly review and remove outdated indexed documents
4. **Backup**: Back up `vectorstore/chroma_db/` if maintaining critical indexes

---

## Advanced Usage

### Batch Processing

To process specific PDFs programmatically:
```python
from src.pdf_chunker import extract_and_chunk_pdf
from src.vector_store import VectorStoreManager

# Process single PDF
chunks = extract_and_chunk_pdf("path/to/document.pdf", 1000, 200)

# Add to vector store
vsm = VectorStoreManager()
vsm.create_or_load()
vsm.add_documents(chunks, source_file="path/to/document.pdf")
```

### Custom Prompts

Modify the prompt template in `src/retriever.py` for specialized use cases:
```python
prompt = f"""You are a technical expert. Use the following context to provide 
a detailed technical answer with examples.

Context:
{context}

Question: {query}

Answer:"""
```

---

## License

MIT License

---

## Acknowledgments

Built with:
- [LangChain](https://github.com/langchain-ai/langchain) - LLM orchestration framework
- [Ollama](https://ollama.ai) - Local LLM inference
- [ChromaDB](https://www.trychroma.com/) - Vector database
- [PyMuPDF](https://pymupdf.readthedocs.io/) - PDF processing

---
