from dotenv import load_dotenv
import os
from pinecone import Pinecone
load_dotenv()
PINECONE_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_HOST = os.getenv('PINECONE_IDX_HOST')
client = Pinecone(api_key=PINECONE_KEY)
index = client.Index(host=PINECONE_HOST)
FILES_ROOT_PATH = os.getenv('FILES_ROOT_PATH')
if not FILES_ROOT_PATH:
    raise ValueError("FILES_ROOT_PATH is not set in environment variables.")

# records = getcsvdata(FILES_ROOT_PATH+'faqs.csv')

# index.upsert_records(
#     namespace= 'try2',
#     records= records
# )