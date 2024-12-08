#8
#observes the performance of both basic and semantic search. 
# Metrics like Mean Reciprocal Rank (MRR) / Precision@K are calculated here to validate the implementation.
# evaluation.py
import numpy as np
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util
from elasticsearch import Elasticsearch

#load precomputed embeddings and data
embeddings = torch.tensor(np.load("embeddings.npy")).to('cpu')  #Load embeddings to CPU
data = pd.read_csv("data_with_ids.csv") #using the updated data with _id
data['processed_text'] = data['processed_text'].fillna('').astype(str)

#SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')  # all-MiniLM-L6-v2 No need to move the model to CUDA

# Elasticsearch connection
es = Elasticsearch("http://localhost:9200")
index_name = "newsgroups"


query_relevant_pairs = { #BETTER QUERIES - BETTER FOR SEMANTIC SEARCH
    "scientific advancements": data[data['target'].isin([11, 12, 13])]['_id'].tolist(), #11,12,13,14
    "emerging technology trends": data[data['target'].isin([1, 2, 3, 4])]['_id'].tolist(), #1,2,3,4,5
} #previously used just "science" and "tehcnology"

# Evaluate basic search
def evaluate_basic_search(query_relevant_pairs, top_k=5): #5
    total_precision = 0
    total_mrr = 0

    for query, relevant_docs in query_relevant_pairs.items():
        relevant_categories = data[data['_id'].isin(relevant_docs)]['target'].unique().tolist()

        query_body = {
            "query": {
                "bool": {
                    "should": [
                        {"match": {"processed_text": query}},
                        {"match_phrase": {"processed_text": {"query": query, "boost": 2}}},
                        {"terms": {"target": relevant_categories}}
                    ],
                    "minimum_should_match": 1
                }
            },
            "size": top_k
        }



        response = es.search(index=index_name, body=query_body)
        #response = es.search(index=index_name, body=query_body, size=top_k)
        hits = response['hits']['hits']

        #extract document IDs
        #retrieved_docs = [int(hit['_id']) for hit in hits]
        retrieved_docs = [hit['_id'] for hit in hits]
        retrieved_docs = list(set(retrieved_docs))  #remove duplicates

        #FOR DEBUGGING
        print(f"Query: {query}")
        #print(f"Retrieved Docs (IDs): {retrieved_docs}")
        #print(f"Relevant Docs (IDs): {relevant_docs}")

        #evaluate Precision@K and MRR
        #relevant_found = [1 if doc_id in relevant_docs else 0 for doc_id in retrieved_docs]
        relevant_found = [1 if str(doc_id) in relevant_docs else 0 for doc_id in retrieved_docs]
        #precision = sum(relevant_found) / top_k
        #precision = sum(relevant_found) / len(retrieved_docs) if retrieved_docs else 0 #prevents p being over 1
        precision = sum(relevant_found) / max(len(retrieved_docs), top_k)
        mrr = sum((1 / (rank + 1)) for rank, found in enumerate(relevant_found) if found)

        total_precision += precision
        total_mrr += mrr

    avg_precision = total_precision / len(query_relevant_pairs)
    avg_mrr = total_mrr / len(query_relevant_pairs)
    print(f"Basic Search - Precision@{top_k}: {avg_precision:.4f}, MRR: {avg_mrr:.4f}")
    return avg_precision, avg_mrr


def preprocess_query(query):
    #extra preprocessing
    query = query.lower()
    query = ' '.join(query.split())
    return query

def evaluate_semantic_search(query_relevant_pairs, top_k=10, cosine_threshold=0.45):
    total_precision = 0
    total_mrr = 0

    for query, relevant_docs in query_relevant_pairs.items():
        query_embedding = model.encode(preprocess_query(query), convert_to_tensor=True).to('cpu')

        #cosine similarity
        cosine_scores = util.pytorch_cos_sim(query_embedding, embeddings)

        #initial top_k results
        initial_top_k = 100
        top_results = torch.topk(cosine_scores[0], k=initial_top_k, largest=True)
        retrieved_docs_initial = top_results.indices.cpu().numpy()

        #Filter by threshold
        filtered_scores_indices = [
            (score.item(), idx) for score, idx in zip(top_results.values, retrieved_docs_initial) if score >= cosine_threshold
        ]
        filtered_scores_indices = sorted(filtered_scores_indices, key=lambda x: -x[0])[:top_k]

        if filtered_scores_indices: #unpack scores
            top_scores, retrieved_docs = zip(*filtered_scores_indices)
            retrieved_doc_ids = [data.iloc[idx]['_id'] for idx in retrieved_docs]
        else:
            top_scores, retrieved_docs, retrieved_doc_ids = [], [], []

        print(f"Query: {query}")
        print(f"Retrieved Docs (IDs): {retrieved_doc_ids}")
        print(f"Cosine Scores: {top_scores}")

        #evaluate Precision@K and MRR
        relevant_found = [1 if doc_id in relevant_docs else 0 for doc_id in retrieved_doc_ids]
        print(f"Relevant Found in Top-K (IDs): {relevant_found}")

        precision = sum(relevant_found) / min(top_k, len(retrieved_doc_ids))
        mrr = sum((1 / (rank + 1)) for rank, found in enumerate(relevant_found) if found)

        total_precision += precision
        total_mrr += mrr

    avg_precision = total_precision / len(query_relevant_pairs)
    avg_mrr = total_mrr / len(query_relevant_pairs)

    print(f"Semantic Search - Precision@{top_k}: {avg_precision:.4f}, MRR: {avg_mrr:.4f}")
    return avg_precision, avg_mrr

#Run on Queries
if __name__ == "__main__":
    print("Evaluating Basic Search...")
    basic_precision, basic_mrr = evaluate_basic_search(query_relevant_pairs)

    print("\nEvaluating Semantic Search...")
    semantic_precision, semantic_mrr = evaluate_semantic_search(query_relevant_pairs)
