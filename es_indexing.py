#4
#indexing docs into elasticsearch
#python p.py

from elasticsearch import Elasticsearch, helpers
import pandas as pd

# Connect to Elasticsearch
print("Connecting to Elasticsearch...")
es = Elasticsearch("http://localhost:9200")
if not es.ping():
    print("Could not connect to Elasticsearch.")
else:
    print("Connected to Elasticsearch.")

# Load preprocessed data
print("Loading preprocessed data...")
# try:
#     data = pd.read_csv("preprocessed_data.csv")  # Ensure the path is correct
#     print(f"Loaded {len(data)} records from preprocessed_data.csv")
# except FileNotFoundError:
#     print("Error: preprocessed_data.csv not found.")
#     exit()
try:
    data = pd.read_csv("data_with_ids.csv")  # Ensure the path is correct
    print(f"Loaded {len(data)} records from data_with_ids.csv")
except FileNotFoundError:
    print("Error: data_with_ids.csv not found.")
    exit()

# Prepare actions for bulk indexing
print("Preparing data for bulk indexing...")
actions = [
    {
        "_index": "newsgroups",
        "_id": row['_id'],
        "_source": {
            "text": row['text'],
            "processed_text": row['processed_text'],
            "target": int(row['target'])
        }
    }
    for _, row in data.iterrows()
]

# Perform bulk indexing
print("Indexing documents...")
try:
    response = helpers.bulk(es, actions, raise_on_error=False, stats_only=False)
    print("Documents indexed successfully.")
except helpers.BulkIndexError as bulk_error:
    print("Bulk indexing error:")
    for error in bulk_error.errors:
        print(error)

# Retrieve documents with their Elasticsearch-generated `_id`
print("Retrieving indexed documents with `_id`...")
try:
    # Use the Elasticsearch scroll API to retrieve all documents
    all_docs = []
    for doc in helpers.scan(es, index="newsgroups"):
        source = doc['_source']
        source['_id'] = doc['_id']  # Add the `_id` field
        all_docs.append(source)

    # Save the retrieved data with `_id` to a CSV file
    data_with_ids = pd.DataFrame(all_docs)
    data_with_ids.to_csv("data_with_ids.csv", index=False)
    print("Saved indexed data with `_id` to 'data_with_ids.csv'.")
except Exception as e:
    print("Error retrieving indexed documents:", e)


# #VERIFIED WITH curl -X GET "http://localhost:9200/newsgroups/_search?pretty&q=*:*&size=1"
