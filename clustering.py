# #6
# This script performs clustering on the preprocessed data and saves cluster labels to Elasticsearch.
# #clustering functionality
#performs clustering on the preprocessed data and save cluster labels to Elasticsearch.
#enhances the search engine with topic-based clustering functionality.

# clustering.py
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.feature_extraction.text import TfidfVectorizer
from elasticsearch import Elasticsearch, helpers

#load preprocessed data
data = pd.read_csv("preprocessed_data.csv")
data = data.dropna(subset=['processed_text']) #drop null texts


#vectorize processed text
tfidf_vectorizer = TfidfVectorizer(max_features=1000) #use top 1000 features for cluster
tfidf_matrix = tfidf_vectorizer.fit_transform(data['processed_text'])

#perform clustering with kmeans
kmeans = KMeans(n_clusters=20, random_state=42) #20 topic clusters
data['cluster'] = kmeans.fit_predict(tfidf_matrix) #add labels to data frame

#Save clusters to elasticsearch
es = Elasticsearch("http://localhost:9200")
actions = [
    {
        "_index": "newsgroups",
        "_id": idx,
        "_source": {
            "text": row['text'],
            "processed_text": row['processed_text'],
            "target": int(row['target']),
            "cluster": int(row['cluster']) #cluster label
        }
    }
    for idx, row in data.iterrows()
]

helpers.bulk(es, actions)
print("Clustering complete and stored in Elasticsearch.")

