import os
from collections import defaultdict
import db.dbops as dbops
import time
from readers.csvreader import getcsvdata
from readers.pdfreader import getpdfchunks
from readers.txtreader import gettxtchunks
from dotenv import load_dotenv
load_dotenv()
PRODUCTION  = os.getenv("PRODUCTION", "false").lower() in ("true", "1", "yes")
FILES_ROOT_PATH = os.getenv('FILES_ROOT_PATH')
if not FILES_ROOT_PATH:
    raise ValueError("FILES_ROOT_PATH is not set in environment variables.")

def grpext(folder_path):
    files_by_ext = defaultdict(list)

    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)

        if os.path.isdir(full_path):
            # skip dir, never come here. no dir in dir. just files
            continue
        ext = os.path.splitext(filename)[1].lower().lstrip('.')

        files_by_ext[ext].append(filename)

    return dict(files_by_ext)

def intialize(reset = None):
    if reset is None:
        return
    if reset:
        dbops.deletenamespace(all=True)
        return
    files = grpext(FILES_ROOT_PATH)
    for ext in files:
        ext = ext.lower()
        for filename in files[ext]:
            if PRODUCTION:
                if 'dummy' in filename:
                    continue
            if ext == 'pdf':
                records = getpdfchunks(FILES_ROOT_PATH+filename)
                dbops.upsertindb(records,filename)
            elif ext == 'txt':
                records = gettxtchunks(FILES_ROOT_PATH+filename)
                dbops.upsertindb(records,filename)
            elif ext == 'csv':
                records = getcsvdata(FILES_ROOT_PATH+filename)
                dbops.upsertindb(records, filename)
            else:
                print(f'Not valid file extention, it must be pdf, csv or txt.')
            time.sleep(1)


def upsetfiles(filewithext):
    temp = filewithext.split('.')
    ext = temp[-1]
    filename = temp[-2]
    ext = ext.lower()
    if ext == 'pdf':
        records = getpdfchunks(FILES_ROOT_PATH+filename)
        dbops.upsertindb(records,filename)
    elif ext == 'txt':
        records = gettxtchunks(FILES_ROOT_PATH+filename)
        dbops.upsertindb(records,filename)
    elif ext == 'csv':
        records = getcsvdata(FILES_ROOT_PATH+filename)
        dbops.upsertindb(records, filename)
    else:
        print(f'Not valid file extention, it must be pdf, csv or txt.')

def upsertrecord(records):
    dbops.upsertindb(records, 'singletone')


def gettopk(query, topk=3, thresold=0.1):
    return dbops.searchindb(query, topk= topk, threshold=thresold)



# print(f'{PRODUCTION=}')
# if not PRODUCTION:
#     intialize(reset=)  <- this will throw error this is intentnal to stop everything
#     q = 'how to refund?'
# print(f'{PRODUCTION=}')
# print(gettopk('how do i get refund?'))
