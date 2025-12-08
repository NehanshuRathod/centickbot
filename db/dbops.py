from db.pineconeDB import index

def upsertindb(records, filename):
    index.upsert_records(
        namespace= filename,
        records= records
    )
    print(f'From {filename} data upserted:{len(records)}\nNamespace:{filename}')

def searchindb(query,topk=3,threshold=0.15):
    namespaces = index.describe_index_stats()['namespaces']
    namespaces = namespaces.keys()
    res = {}
    for n in namespaces:
        result = index.search(
            namespace=n,
            query={
                'top_k':topk,
                'inputs':{
                    'text':query
                }
            }
        )
        if 'csv' not in n:
            topk+=2
        result = result['result']['hits']
        # print(result)
        for reply in result:
            # print(reply)
            if reply['_score']<threshold:
                continue
            reply = reply['fields']
            text = " --- ".join(reply.values())
            # print(text)
            if n not in res:
                res[n] = [text]
            else:
                res[n].append(text)

    return res

def deletenamespace(namespace_to_delete=[], all = False):
    namespaces = index.describe_index_stats()['namespaces']
    namespaces = namespaces.keys()
    if all:
        namespace_to_delete = namespaces
    for names in namespace_to_delete: 
        if all or names in namespaces:
            index.delete(delete_all=True, namespace=names)
            print(f"Namespace '{names}' has been deleted.")
