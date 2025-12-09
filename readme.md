# Chatbot API (FastAPI)

This backend provides a secure chatbot API with a single endpoint: `/chat`.

## 📌 Requirements

- Python 3.10+
- Redis server (for rate limiting)

## 🚀 Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the API
uvicorn main:app --reload
