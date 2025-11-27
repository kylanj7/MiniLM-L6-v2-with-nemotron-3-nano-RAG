# Lightweight RAG Setup Checklist

## 1. Environment Setup
- [ ] Python 3.10+ installed
- [ ] Virtual environment created (`python -m venv venv`)
- [ ] Virtual environment activated
- [ ] Git repository initialized (optional)

## 2. Ollama Setup
- [ ] Ollama installed on system ([ollama.ai](https://ollama.ai))
- [ ] Ollama service running (`ollama serve`)
- [ ] TinyLlama model pulled (`ollama pull tinyllama:1.1b`)
- [ ] Embedding model pulled (`ollama pull gemma:2b`)
- [ ] Test Ollama API accessible at `http://localhost:11434`

## 3. Dependencies Installation
- [ ] Create `requirements.txt` with:
```
  langchain
  langchain-ollama
  langchain-chroma
  langchain-text-splitters
  pypdf
  chromadb
```
- [ ] Install dependencies (`pip install -r requirements.txt`)

## 4. Directory Structure
- [ ] Create `config/` directory
- [ ] Create `data/pdfs/` directory
- [ ] Create `vectorstore/` directory (will auto-populate)
- [ ] Create `src/` directory
- [ ] Create `utils/` directory (optional)
- [ ] Create `notebooks/` directory (optional)

## 5. Core Files to Create
- [ ] `config/__init__.py` (empty file)
- [ ] `config/settings.py` (configuration module)
- [ ] `src/__init__.py` (empty file)
- [ ] `src/pdf_chunker.py` (your existing chunker - **replace PyMuPDF with pypdf**)
- [ ] `src/embeddings.py` (Ollama embeddings interface)
- [ ] `src/vector_store.py` (ChromaDB manager)
- [ ] `src/retriever.py` (RAG query logic)
- [ ] `main.py` (CLI interface)
- [ ] `.gitignore`
- [ ] `README.md`
- [ ] `LICENSE` (proprietary license)

## 6. Configuration Files
- [ ] `.gitignore` should include:
```
  __pycache__/
  *.py[cod]
  venv/
  .env
  vectorstore/
  data/pdfs/*.pdf
  chunks_output.txt
  *.log
  .DS_Store
```

## 7. Data Preparation
- [ ] Add sample PDFs to `data/pdfs/` directory
- [ ] Verify PDFs are readable (not scanned images)
- [ ] Check PDF file permissions

## 8. Testing & Validation
- [ ] Test PDF chunking works (`python src/pdf_chunker.py`)
- [ ] Test embeddings generation (simple script)
- [ ] Test ChromaDB can create collection
- [ ] Test Ollama LLM responds to prompts
- [ ] Run end-to-end indexing
- [ ] Run test query and validate response

## 9. Security Considerations
- [ ] Ensure `vectorstore/` is gitignored (contains embedded data)
- [ ] Ensure `data/pdfs/` is gitignored (sensitive documents)
- [ ] Verify all data stays local (no external API calls)
- [ ] Consider disk encryption for sensitive data
- [ ] Document data retention policies

## 10. Performance Optimization
- [ ] Verify multiprocessing works on target laptops
- [ ] Test memory usage during indexing
- [ ] Test memory usage during queries
- [ ] Benchmark query response times
- [ ] Adjust `CHUNK_SIZE` and `CHUNK_OVERLAP` if needed

## 11. Documentation
- [ ] Document installation steps in README
- [ ] Document how to add new PDFs
- [ ] Document how to query the system
- [ ] Document how to reset/rebuild vector store
- [ ] Add usage examples
- [ ] Add licensing terms and contact info

## 12. Deployment Readiness
- [ ] Create deployment script/instructions
- [ ] Test on clean laptop environment
- [ ] Verify Ollama auto-starts (or document manual start)
- [ ] Create troubleshooting guide
- [ ] Set up logging for debugging
- [ ] Add proprietary license file
- [ ] Remove or replace AGPL dependencies (PyMuPDF)

---

## Quick Verification Commands

Once setup:
```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Check Python environment
python --version
pip list | grep langchain

# Test structure
ls -R lightweight-rag/

# Count PDFs
ls data/pdfs/*.pdf | wc -l
```

## Priority Order
- **Critical (Start Here)**: Items 1-5
- **Initial Testing**: Items 6-8  
- **Pre-Production**: Items 9-11
- **Before Commercial Deployment**: Item 12

---

## License Compliance Check
- [ ] Verify no AGPL dependencies remain (check `pip list`)
- [ ] All dependencies are MIT/BSD/Apache licensed
- [ ] Proprietary license file added to root directory
- [ ] Copyright notices preserved for open-source dependencies
