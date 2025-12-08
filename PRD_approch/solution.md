NUTSHELL

- **[DONE !]** Data Gathering: Read and preprocess the data. FAQ retrived

- **[DONE !]** Embedding: Use Sentence-BERT to generate dense vector embeddings for both the document and user queries.
- **[DONE !]** Vector DB: Store document embeddings in a FAISS or Pinecone index for fast retrieval.
User Query: Convert the user’s query into an embedding.
- **[DONE !]** Retrieve Top-k: Use vector search to find the top-k most relevant document chunks.
- NLP Generation: Use a model to generate a response, either by concatenating chunks or refining them.
API: Expose everything via a FastAPI endpoint for easy querying

```
You are an assistant that provides only factual answers based strictly on the context provided below. Do not add any extra commentary. If the context does not have enough information to answer the user's question, respond with: "I do not have enough information to answer that. Please rephrase your query."

Question: How do I reset my password?

Context:
1. To reset your password, go to the password recovery page and enter your email address.
2. You will receive a password reset link in your inbox. If you don’t see it, check your spam folder.
3. If you do not receive the email after a few minutes, try resending the reset request.
4. For further assistance, contact customer support.

Answer:
```