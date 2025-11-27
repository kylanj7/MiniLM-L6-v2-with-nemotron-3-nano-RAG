"""
ChromaDB vector store management with incremental indexing
"""
from langchain_chroma import Chroma
from src.embeddings import get_embeddings
from config.settings import VECTOR_STORE_DIR, COLLECTION_NAME
import json
from pathlib import Path
import hashlib


class VectorStoreManager:
    """Manages ChromaDB vector store operations with file tracking"""
    
    def __init__(self):
        self.embeddings = get_embeddings()
        self.vector_store = None
        self.index_log_path = VECTOR_STORE_DIR / "indexed_files.json"
        self.indexed_files = self._load_index_log()
    
    def _load_index_log(self):
        """Load log of previously indexed files."""
        if self.index_log_path.exists():
            with open(self.index_log_path, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_index_log(self):
        """Save log of indexed files."""
        self.index_log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.index_log_path, 'w') as f:
            json.dump(self.indexed_files, f, indent=2)
    
    def _file_hash(self, filepath):
        """Generate hash of file for change detection."""
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def is_file_indexed(self, pdf_path):
        """Check if file is already indexed and unchanged."""
        filename = Path(pdf_path).name
        
        if filename not in self.indexed_files:
            return False
        
        current_hash = self._file_hash(pdf_path)
        return self.indexed_files[filename] == current_hash
    
    def mark_file_indexed(self, pdf_path):
        """Mark file as indexed with its hash."""
        filename = Path(pdf_path).name
        self.indexed_files[filename] = self._file_hash(pdf_path)
        self._save_index_log()
    
    def create_or_load(self):
        """Load existing vector store or create new one."""
        print(f"Loading vector store from {VECTOR_STORE_DIR}...")
        
        self.vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=self.embeddings,
            persist_directory=str(VECTOR_STORE_DIR)
        )
        
        print(f"✓ Vector store loaded: {COLLECTION_NAME}")
        return self.vector_store
    
    def add_documents(self, chunks, source_file=None, batch_size=100):
        """
        Add document chunks to vector store in batches.
        
        Args:
            chunks: List of LangChain Document objects
            source_file: Optional path to source PDF for tracking
            batch_size: Number of chunks to process at once
        """
        if not self.vector_store:
            self.create_or_load()
        
        print(f"Adding {len(chunks)} chunks in batches of {batch_size}...")
        
        all_ids = []
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            batch_num = i // batch_size + 1
            total_batches = (len(chunks) - 1) // batch_size + 1
            print(f"  Processing batch {batch_num}/{total_batches}")
            
            ids = self.vector_store.add_documents(batch)
            all_ids.extend(ids)
        
        print(f"✓ Added {len(all_ids)} chunks successfully")
        
        # Mark file as indexed if source provided
        if source_file:
            self.mark_file_indexed(source_file)
        
        return all_ids
    
    def similarity_search(self, query, k=3):
        """Retrieve k most similar chunks."""
        if not self.vector_store:
            self.create_or_load()
        
        return self.vector_store.similarity_search(query, k=k)
    
    def get_collection_count(self):
        """Get number of documents in collection."""
        if not self.vector_store:
            self.create_or_load()
        
        return self.vector_store._collection.count()
    
    def delete_collection(self):
        """Delete the entire collection and index log."""
        if self.vector_store:
            self.vector_store.delete_collection()
            print(f"✓ Deleted collection: {COLLECTION_NAME}")
        
        # Clear index log
        self.indexed_files = {}
        self._save_index_log()
        print("✓ Cleared index log")
    
    def list_indexed_files(self):
        """Return list of indexed files."""
        return list(self.indexed_files.keys())
