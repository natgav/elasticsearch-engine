#4
#indexing docs into elasticsearch
# from elasticsearch import Elasticsearch, helpers
# import pandas as pd

# connect to Elasticsearch
# es = Elasticsearch("http://localhost:9200")
# index_name = "newsgroups"

# load preprocessed data
# data = pd.read_csv("preprocessed_data.csv")

# indexing docs
# actions = [
#     {
#         "_index": index_name,
#         "_source": {
#             "processed_text": row['processed_text'],
#             "target": int(row['target'])
#         }
#     }
#     for _, row in data.iterrows()
# ]

# helpers.bulk(es, actions)
# print("Documents indexed successfully.")

#python p.py
from elasticsearch import Elasticsearch, helpers
import pandas as pd

#connect to ES
print("Connecting to Elasticsearch...")
es = Elasticsearch("http://localhost:9200")
if not es.ping():
    print("Could not connect to Elasticsearch.")
else:
    print("Connected to Elasticsearch.")

#load preprocessed data
print("Loading preprocessed data...")
try:
    data = pd.read_csv("../preprocessed_data.csv") #path verified
    print(f"Loaded {len(data)} records from preprocessed_data.csv")
except FileNotFoundError:
    print("Error: preprocessed_data.csv not found.")
    exit()

#prepare actions for bulk indexing
print("Preparing data for bulk indexing...")
actions = [
    {
        "_index": "newsgroups",
        "_source": {
            "text": row['text'],
            "processed_text": row['processed_text'],
            "target": int(row['target'])
        }
    }
    for _, row in data.iterrows()
]

#perform bulk indexing
print("Indexing documents...")
try:
    #extra details for failed docs
    response = helpers.bulk(es, actions, raise_on_error=False, stats_only=False)
    print("Documents indexed successfully.")
except helpers.BulkIndexError as bulk_error:
    print("Bulk indexing error:")
    for error in bulk_error.errors:
        print(error)



#VERIFIED WITH curl -X GET "http://localhost:9200/newsgroups/_search?pretty&q=*:*&size=1"
