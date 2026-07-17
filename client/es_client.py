from assistant.rag.doc_manager import load_documents
from assistant.rag.es_manager import bulk_insert_es, create_es_client, ES_INDEX, create_index

if __name__ == '__main__':
    es_client = create_es_client()
    res = es_client.indices.exists(index=ES_INDEX)
    print(res)

    create_index(client=es_client)

    # docs = load_documents("rds")
    # print(docs[:5])
    #
    # bulk_insert_es(docs)