# 8dec 2025

- working on embedding and pinecone unsperting
- pinecone namespaces, and search query
- connect everything, 
-  **note: `connector.py` this is final script where evrything will be connected and api will interact on this file**
```.env
.env
PINECONE_API_KEY='apikey'
PINECONE_IDX_HOST = 'idxhostlink'
PRODUCTION='false' <- true while deplyoung
FILES_ROOT_PATH ='data\\' <- vary
```

- **CHECKPOINT** - getting topk from db is done!!

# 7dec 2025
- understand pinecone db, how it works, mainly `pinecone` lib
- pinecone does embedding thing, no need for external embeddinf models
- droped idea of `FAISS` for inital phase and shifted directly to `pinecone` -> effective + alredy in use
- based on pinecone upsert change reader files. 
- changes `list[str]` -> `list[dict['id': , 'text':]]`

- new effective approch - shfted from `tiktoken` to normal `word based chunking` -> **reduce depedenacies** (main thing)

# 6 dec 2025
- scripted readers for bot. This utility will read files, data retrieved from files via this reader will be embedded
- normalised data to be veoctorised

- csv to string list
- `PyPDF2` used ot parse pdf
- csv, txt, pdf can be used.
- `readers\csvreader.py` `readers\txtreader.py` `reader\pdfreader` used tiktoken to get chunks 


# 5th Dec 2025

- Scrapped using selenuim.immented `faq_scraper.py` to gather info, like FAQs.

- Storeed it in faqs.cvs- enhanced `faq_scraper.py` using gpt - > added comments and better error handling.
- Imented `tnc_scraper.py` - > tnc.csv
- `policy_sraper.py` - > policy.csv
- Data gathering done for initial phase done.
- cvs formate `section` - > `Clause Content`
- `..\scraper\..` will be update via ci/cd pipeline after every update in site. (corn job / manual -  optional)

# 4th dec 2025 

- Got `Chatbot Architecture.docx`
- understand client req and problem, and current solution.

- Build an MVP type system arctitecture - MY APPORCH

![CentickBOTv1](https://raw.githubusercontent.com/jyotraval/centickbot/refs/heads/main/PRD_approch/CentickBOTv1.png)
