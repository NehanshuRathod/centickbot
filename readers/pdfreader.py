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


# import tiktoken
from PyPDF2 import PdfReader
import os


def clean_text(t):
    if not t:
        return ""
    t = t.replace("\n", " ").replace("\t", " ")
    return " ".join(t.split())

def getpdfchunks(pdf_path, chunk_size=150, overlap=50):
    reader = PdfReader(pdf_path)
    full_text = "".join([page.extract_text() or "" for page in reader.pages])
    full_text = clean_text(full_text)

    words = full_text.split()
    chunks = []
    start = 0
    base = os.path.splitext(os.path.basename(pdf_path))[0]
    counter = 1

    while start < len(words):
        end = start + chunk_size
        chunk_text = " ".join(words[start:end])
        chunks.append({"_id": f"{base}_{counter}", "text": chunk_text})
        counter += 1
        start += chunk_size - overlap

    return chunks


# pdf_path = "data\\dummyearth.pdf"
# chunks = getpdfchunks(pdf_path, chunk_size=150, overlap=50)

# print(f"Created {len(chunks)} chunks")
# print(chunks[0] ,chunks[1] ,chunks[2], sep='\n\n')

