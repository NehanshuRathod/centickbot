import tiktoken

def chunk_text_tokens(file_path, model="text-embedding-3-small", chunk_size=500, overlap=200):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    text = text.replace("\n", " ")
    # for .md formate directly
    text = text.replace("*", " ")
    text = text.replace("#", " ")   
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    
    chunks = []
    start = 0
    while start < len(tokens):
        end = start + chunk_size
        chunk_tokens = tokens[start:end]
        chunk_text = encoding.decode(chunk_tokens)
        chunks.append(chunk_text)
        start += chunk_size - overlap  # slide the window
    
    return chunks

# txt_path = "data/dummylaptop.txt"
# chunks = chunk_text_tokens(txt_path, chunk_size=500, overlap=200)

# print(f"Created {len(chunks)} chunks")
# print(chunks[0] ,chunks[1] ,chunks[2], sep='\n\n')