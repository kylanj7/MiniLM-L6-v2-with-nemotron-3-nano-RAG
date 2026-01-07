# app.py

import streamlit as st
import os
from src.retriever import RAGRetriever

st.set_page_config(
    page_title="Nemotron-RAG",
    page_icon="💻",
    layout="wide"
)


def check_password():
    """Simple password protection for the RAG system."""
    def password_entered():
        # You can change this password or set RAG_PASSWORD environment variable
        correct_password = os.getenv("RAG_PASSWORD", "nemotron2024")
        if st.session_state["password"] == correct_password:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.title("💻 Nemotron-3-30B & Mini-L6-v2 RAG")
        st.markdown("### 🔐 Authentication Required")
        st.text_input("Enter password:", type="password", on_change=password_entered, key="password")
        st.caption("Contact admin for access")
        return False
    elif not st.session_state["password_correct"]:
        st.title("💻 Nemotron-3-30B & Mini-L6-v2 RAG")
        st.markdown("### Authentication Required")
        st.text_input("Enter password:", type="password", on_change=password_entered, key="password")
        st.error(" Incorrect password")
        return False
    else:
        return True

@st.cache_resource
def load_pipeline():
    """Cache the RAG pipeline to avoid reloading on each interaction."""
    return RAGRetriever()

def main():
    if not check_password():
        st.stop()

    st.title("💻 Nemotron-3-30B & Mini-L6-v2 RAG")
    st.caption("Local inference RAG")

    # Initialize pipeline
    with st.spinner("Loading models..."):
        pipeline = load_pipeline()

    # Sidebar for settings display
    with st.sidebar:
        st.header("⚙️  Configuration")
        st.text(f"LLM: Nemotron-3-30B")
        st.text(f"GPUs: 3090 & 3090ti")
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
    if query := st.chat_input("Ask a question..."):
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
