from PyPDF2 import PdfReader

# reader = PdfReader("data\\dummydata.pdf")
# text = ""
# for page in reader.pages:
#     text += page.extract_text() or ""

# print(text)

# chunk_size = 500
# overlap = 150
# chunks = []

# full_text = "".join([page.extract_text().replace('\n','') or "" for page in reader.pages])

# start = 0
# while start < len(full_text):
#     end = start + chunk_size
#     chunk = full_text[start:end]
#     chunks.append(chunk)
#     start += chunk_size - overlap  # move forward with overlap

# print(f"chunks lenght: {len(chunks)}")
# print(chunks[0])
# print(chunks[1])
# print(chunks[2])


import tiktoken


def getchunks(pdf_path, model="all-MiniLM-L6-v2", chunk_size=500, overlap=200):
    reader = PdfReader(pdf_path)
    full_text = "".join([page.extract_text() or "" for page in reader.pages])
    full_text = full_text.replace("\n", " ")



    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(full_text)
    
    chunks = []
    start = 0
    while start < len(tokens): # slingind window approch
        end = start + chunk_size
        chunk_tokens = tokens[start:end]
        chunk_text = encoding.decode(chunk_tokens)
        chunks.append(chunk_text)
        start += chunk_size - overlap 
    
    return chunks

# pdf_path = "data\\dummyearth.pdf"
# chunks = getchunks(pdf_path,model="text-embedding-3-small", chunk_size=300, overlap=100)

# print(f"Created {len(chunks)} chunks")
# print(chunks[0] ,chunks[1] ,chunks[2], sep='\n\n')

