import os

def clean_text(t):
    if not t:
        return ""
    t = t.replace("\n", " ").replace("\t", " ")
    t = t.replace("*", " ").replace("#", " ")
    return " ".join(t.split())


def gettxtchunks(file_path, chunk_size=150, overlap=50):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    
    text = clean_text(text)
    words = text.split()

    chunks = []
    start = 0
    base = os.path.splitext(os.path.basename(file_path))[0]
    counter = 1

    while start < len(words):
        end = start + chunk_size
        chunk_text = " ".join(words[start:end])
        chunks.append({"_id": f"{base}_{counter}", "text": chunk_text})
        counter += 1
        start += chunk_size - overlap  # sliding window

    return chunks


# txt_path = "data/dummylaptop.txt"
# chunks = gettxtchunks(txt_path, chunk_size=150, overlap=50)
# print(f"Created {len(chunks)} chunks")
# print(chunks[0] ,chunks[1] ,chunks[2], sep='\n\n')