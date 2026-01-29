# 🔄 Mistral Self-Correcting RAG

A RAG chatbot that self-evaluates and auto-corrects its answers, using Mistral API.

<img width="1914" height="852" alt="image" src="https://github.com/user-attachments/assets/077c8d27-dd28-4e24-bb0b-3e0570ce7273" />


##  Concept

1. **Answers** questions based on your PDFs
2. **Self-evaluates** (fidelity + relevance /20)
3. **Auto-corrects** if the score is too low

## Architecture

PDF → Chunking → Embeddings (mistral-embed) → ChromaDB
↓
Question → Semantic Search → Generation (Mistral)
↓
Evaluation (Judge Mistral)
↓
Score < 14 ? → Retry with more context
↓
Final answer + scores


## Stack

- **LLM**: Mistral AI API
- **Embeddings**: mistral-embed
- **Vector DB**: ChromaDB
- **Interface**: Streamlit

## Installation
# 1 : clone repo and install dependencies
```bash
git clone https://github.com/your-username/mistral-self-correcting-rag.git
cd mistral-self-correcting-rag
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

# 2 : Create .env and add your API key
```bash
MISTRAL_API_KEY=your_key_here
```

# 3 : Run
```
streamlit run app.py
```



