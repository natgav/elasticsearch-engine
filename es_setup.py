#3
#set up elasticsearch and create index
#start ES with /opt/homebrew/opt/elasticsearch-full/bin/elasticsearch
#/opt/homebrew/opt/elasticsearch-full/bin/elasticsearch
#TO STOP: brew services stop elasticsearch-full

from elasticsearch import Elasticsearch, exceptions

#connect to ES
try:
    es = Elasticsearch("http://localhost:9200")
    if not es.ping():
        print("Connection to Elasticsearch failed.")
except exceptions.ConnectionError:
    print("Could not connect to Elasticsearch. Is it running?")

#define index name and settings
index_name = "newsgroups"
index_settings = {
    "settings": {
        "analysis": {
            "analyzer": {
                "default": {
                    "type": "standard"
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "text": {"type": "text"},
            "processed_text": {"type": "text"},
            "target": {"type": "integer"}
        }
    }
}

#create the index if it doesn't exist
try:
    if not es.indices.exists(index=index_name):
        response = es.indices.create(index=index_name, body=index_settings)
        print(f"Index '{index_name}' created successfully.")
        print("Response:", response)
    else:
        print(f"Index '{index_name}' already exists.")
except exceptions.RequestError as e:
    print("Error creating index:", e.info)


#MANUALLY INJECTED THE INDEX USING
# curl -X PUT "http://localhost:9200/newsgroups?pretty" -H 'Content-Type: application/json' -d'
# {
#   "settings": {
#     "analysis": {
#       "analyzer": {
#         "default": {
#           "type": "standard"
#         }
#       }
#     }
#   },
#   "mappings": {
#     "properties": {
#       "text": { "type": "text" },
#       "processed_text": { "type": "text" },
#       "target": { "type": "integer" }
#     }
#   }
# }
# '
#VERIFIED WITH
#curl -X GET "http://localhost:9200/newsgroups?pretty"

