#7
#Implement semantic search using embeddings. 
#builds on top of the search engine to provide deeper understanding and more relevant results.
# semantic_search.py
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import numpy as np
import torch 

# Load preprocessed data
# data = pd.read_csv("preprocessed_data.csv")
# data['processed_text'] = data['processed_text'].fillna('').astype(str)
data = pd.read_csv("data_with_ids.csv")  # Load data with `_id`
data['processed_text'] = data['processed_text'].fillna('').astype(str)
# Ensure alignment of embeddings with `_id`
data = data[data['processed_text'].str.split().str.len() > 2] #remove really short texts
data.reset_index(drop=True, inplace=True)  # Reset the DataFrame index to align with embeddings


# Load SentenceTransformer model all-mpnet-base-v2
model = SentenceTransformer('all-MiniLM-L6-v2') #all-MiniLM-L6-v2
embeddings = model.encode(data['processed_text'], convert_to_tensor=True)
# Save embeddings for evaluation
np.save("embeddings.npy", embeddings.cpu().numpy())
print("Embeddings saved to 'embeddings.npy'")

#perform semantic search
def semantic_search(query, top_k=5, char_limit=300):
    
    query_embedding = model.encode(query, convert_to_tensor=True)
    cosine_scores = util.pytorch_cos_sim(query_embedding, embeddings)

    #get top results with scores
    top_results = torch.topk(cosine_scores[0], k=top_k + 10, largest=True)  # buffer for duplicates
    retrieved_docs = top_results.indices.cpu().numpy()
    scores = top_results.values.cpu().numpy()

    #rem. duplicates
    seen_texts = set()
    unique_results = []

    for idx, score in zip(retrieved_docs, scores):
        text = data.iloc[idx]['processed_text']
        if text not in seen_texts:
            unique_results.append((idx, score, text))
            seen_texts.add(text)
        if len(unique_results) == top_k:  #stop after top k unique results
            break

    #print results
    print(f"Top {top_k} Results for Query: '{query}'\n")
    for rank, (idx, score, text) in enumerate(unique_results):
        print(f"Score: {score:.4f}")
        print(f"Text: {text[:char_limit]}{'...' if len(text) > char_limit else ''}\n")
    
    # query_embedding = model.encode(query, convert_to_tensor=True)
    # cosine_scores = util.pytorch_cos_sim(query_embedding, embeddings)
    # top_results = np.argsort(-cosine_scores[0].cpu().numpy())[:top_k]

    # print(f"Top {top_k} Results for Query: '{query}'")
    # for idx in top_results:
    #     score = cosine_scores[0][idx].item()
    #     text = data.iloc[idx]['processed_text']
    #     print(f"\nScore: {score:.4f}")
    #     print(f"Text: {text[:char_limit]}{'...' if len(text) > char_limit else ''}\n")

#run semantic search
if __name__ == "__main__":
    test_query = "science"  #science is our sample testing query
    semantic_search(test_query, top_k=5, char_limit=300)
