"""
Main CLI interface for Lightweight Enterprise RAG System
"""
import sys
import os
import glob
from src.pdf_chunker import process_pdfs_in_directory_parallel, extract_and_chunk_pdf
from src.vector_store import VectorStoreManager
from src.retriever import RAGRetriever
from config.settings import DATA_DIR, CHUNK_SIZE, CHUNK_OVERLAP


def index_documents(force_reindex=False):
    """Index new/changed PDFs only (unless force_reindex=True)."""
    print("=" * 60)
    print("INDEXING DOCUMENTS")
    print("=" * 60)
    
    vsm = VectorStoreManager()
    vsm.create_or_load()
    
    # Get all PDFs
    pdf_files = glob.glob(os.path.join(DATA_DIR, '*.pdf'))
    
    if not pdf_files:
        print("\nNo PDFs found in data/pdfs/ directory.")
        return
    
    # Filter to new/changed files only
    if not force_reindex:
        files_to_process = [f for f in pdf_files if not vsm.is_file_indexed(f)]
        
        if not files_to_process:
            print("\nAll PDFs already indexed. No new files to process.")
            print(f"  Total indexed files: {len(vsm.list_indexed_files())}")
            print("\nUse 'python3 main.py index --force' to re-index everything.")
            return
        
        skipped = len(pdf_files) - len(files_to_process)
        if skipped > 0:
            print(f"Skipping {skipped} already-indexed file(s)")
        
        print(f"Processing {len(files_to_process)} new/changed file(s):\n")
    else:
        files_to_process = pdf_files
        print(f"Force re-indexing ALL {len(files_to_process)} PDF(s)\n")
    
    # Process each file individually
    total_new_chunks = 0
    for pdf_file in files_to_process:
        filename = os.path.basename(pdf_file)
        print(f"Processing: {filename}")
        
        chunks = extract_and_chunk_pdf(pdf_file, CHUNK_SIZE, CHUNK_OVERLAP)
        
        if chunks:
            vsm.add_documents(chunks, source_file=pdf_file, batch_size=100)
            total_new_chunks += len(chunks)
            print(f"  Added {len(chunks)} chunks from {filename}\n")
        else:
            print(f"  Warning: No chunks generated from {filename}\n")
    
    total_docs = vsm.get_collection_count()
    print(f"Indexing complete!")
    print(f"  New chunks added: {total_new_chunks}")
    print(f"  Total chunks in database: {total_docs}")
    print(f"  Indexed files: {len(vsm.list_indexed_files())}")


def query_system():
    """Interactive query interface."""
    print("=" * 60)
    print("RAG QUERY SYSTEM")
    print("=" * 60)
    print("Type 'exit' or 'quit' to stop\n")
    
    rag = RAGRetriever()
    
    while True:
        query = input("\nYour question: ").strip()
        
        if query.lower() in ['exit', 'quit', 'q']:
            print("\nGoodbye!")
            break
        
        if not query:
            continue
        
        result = rag.retrieve_and_generate(query)
        
        print(f"\nAnswer:\n{result['answer']}")
        print(f"\nSources: {', '.join(result['sources'])}")
        print("-" * 60)


def show_stats():
    """Show vector store statistics."""
    vsm = VectorStoreManager()
    vsm.create_or_load()
    
    count = vsm.get_collection_count()
    indexed_files = vsm.list_indexed_files()
    
    print(f"\nVector Store Statistics")
    print(f"  Collection: {COLLECTION_NAME}")
    print(f"  Total chunks: {count}")
    print(f"  Indexed files: {len(indexed_files)}")
    
    if indexed_files:
        print(f"\nIndexed Files:")
        for i, filename in enumerate(sorted(indexed_files), 1):
            print(f"  {i}. {filename}")


def reset_database():
    """Delete and reset the vector store."""
    confirm = input("WARNING: Are you sure you want to delete all indexed documents? (yes/no): ")
    
    if confirm.lower() == 'yes':
        vsm = VectorStoreManager()
        vsm.create_or_load()
        vsm.delete_collection()
        print("Database reset complete")
    else:
        print("Cancelled")


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("Lightweight Enterprise RAG System")
        print("\nUsage:")
        print("  python3 main.py index           - Index new/changed PDFs only")
        print("  python3 main.py index --force   - Re-index all PDFs")
        print("  python3 main.py query           - Start interactive Q&A")
        print("  python3 main.py stats           - Show database statistics")
        print("  python3 main.py reset           - Reset vector database")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'index':
        force = '--force' in sys.argv
        index_documents(force_reindex=force)
    elif command == 'query':
        query_system()
    elif command == 'stats':
        show_stats()
    elif command == 'reset':
        reset_database()
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
