# app.py

import streamlit as st
from src.retriever import RAGRetriever

st.set_page_config(
    page_title="RAG Document Q&A",
    page_icon="📄",
    layout="wide"
)

@st.cache_resource
def load_pipeline():
    """Cache the RAG pipeline to avoid reloading on each interaction."""
    return RAGRetriever()

def main():
    st.title("📄 Document Q&A")
    st.caption("Powered by Phi-3.5 + BGE Reranker")

    # Initialize pipeline
    with st.spinner("Loading models..."):
        pipeline = load_pipeline()

    # Sidebar for settings display
    with st.sidebar:
        st.header("⚙️ Configuration")
        st.text(f"LLM: Phi-3.5-mini-instruct")
        st.text(f"GPUs: 2x RTX 3090")
        st.text(f"Reranking: Enabled")

        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()

    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "sources" in msg:
                with st.expander("📚 Sources"):
                    for src in msg["sources"]:
                        st.markdown(f"- {src}")

    # Query input
    if query := st.chat_input("Ask a question about your documents..."):
        st.session_state.messages.append({"role": "user", "content": query})

        with st.chat_message("user"):
            st.markdown(query)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Adjust this call to match your pipeline's method
                response = pipeline.retrieve_and_generate(query)

                # Handle response format - adjust based on your return type
                if isinstance(response, dict):
                    answer = response.get("answer", str(response))
                    sources = response.get("sources", [])
                else:
                    answer = str(response)
                    sources = []

                st.markdown(answer)

                if sources:
                    with st.expander("📚 Sources"):
                        for src in sources:
                            st.markdown(f"- {src}")

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "sources": sources
        })

if __name__ == "__main__":
    main()
