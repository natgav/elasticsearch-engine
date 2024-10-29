#5
#implement and test searching functionality
from elasticsearch import Elasticsearch

#connect to ES
es = Elasticsearch("http://localhost:9200")
index_name = "newsgroups"

#search query
def search_documents(query_text):
    # query = {
    #     "query": {
    #         "match": {"processed_text": query_text}
    #     }
    # }
    query = {
    "query": {
        "match": {"processed_text": query_text}
    },
    "highlight": {
        "fields": {
            "processed_text": {} #emphasizes search term in returned snippets
        }
    }
}

    response = es.search(index=index_name, body=query)
    for hit in response['hits']['hits']:
        print(f"Score: {hit['_score']}, Text: {hit['_source']['processed_text'][:100]}...\n")

#testing with query science
search_documents("science")

#start ES with /opt/homebrew/opt/elasticsearch-full/bin/elasticsearch
#or just elasticsearch
