import streamlit as st
import os

from rag.pipeline import ask

from rag.retriever import index_documents
from rag.document_loader import load_pdf

st.set_page_config(page_title="Mistral Self-Correcting RAG")
st.title("Mistral Self-Correcting RAG")

# Max attempts
st.sidebar.header("Max attempts")
max_attempts = st.sidebar.number_input("Max attempts", min_value=1, max_value=10, value=2, step=1)

with st.sidebar:
    st.header("Uploading documents")
    uploaded_docs = st.file_uploader("Upload documents", type=["pdf"],accept_multiple_files=True)
    if uploaded_docs:  # Liste non vide
        saved_paths = []
        
        for uploaded_doc in uploaded_docs:
            save_folder = os.path.join(os.getcwd(), "pdfs")
            os.makedirs(save_folder, exist_ok=True)
            save_path = os.path.join(save_folder, uploaded_doc.name)
            
            with open(save_path, "wb") as f:
                f.write(uploaded_doc.getbuffer())
            
            saved_paths.append(save_path)
        
        st.success(f"{len(saved_paths)} files uploaded")
        
        if st.button("Index documents"):
            with st.spinner("Indexing documents..."):
                docs = load_pdf(saved_paths) 
                index_documents(docs)
                st.success("Documents indexed successfully in ChromaDB")

# Chat


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "scores" in message:
                col1, col2 = st.columns(2)
                col1.metric("Fidelity", f"""{message['scores']['fidelity']}/20""")
                col2.metric("Relevance", f"""{message['scores']['relevance']}/20""")

if prompt := st.chat_input("Ask a question"):
    # L'utilisateur a envoyé un message
    # Ajouter le message à la liste des messages
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Appeler la fonction ask
    with st.spinner("Answering..."):
        result = ask(prompt, max_attempts=max_attempts)
    print(result["attempts"])
    # Ajouter le message à la liste des messages
    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "scores": result["evaluation"] 
    })
    col1, col2 = st.columns(2)
    col1.metric("Fidelity", f"{result['evaluation']['fidelity']}/20")
    col2.metric("Relevance", f"{result['evaluation']['relevance']}/20")
    st.rerun()

