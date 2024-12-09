python3 RUN_ALL.py
Running es_setup.py...
/Users/nataliegavin/Desktop/CS 410/FINAL_PROJECT/elasticsearch/es_setup.py:12: ElasticsearchWarning: Elasticsearch built-in security features are not enabled. Without authentication, your cluster could be accessible to anyone. See https://www.elastic.co/guide/en/elasticsearch/reference/7.17/security-minimal-setup.html to enable security.
  if not es.ping():
/Users/nataliegavin/Desktop/CS 410/FINAL_PROJECT/elasticsearch/es_setup.py:40: ElasticsearchWarning: Elasticsearch built-in security features are not enabled. Without authentication, your cluster could be accessible to anyone. See https://www.elastic.co/guide/en/elasticsearch/reference/7.17/security-minimal-setup.html to enable security.
  if not es.indices.exists(index=index_name):
Index 'newsgroups' already exists.

es_setup.py executed successfully.

Running es_indexing.py...
Connecting to Elasticsearch...
/Users/nataliegavin/Desktop/CS 410/FINAL_PROJECT/elasticsearch/es_indexing.py:11: ElasticsearchWarning: Elasticsearch built-in security features are not enabled. Without authentication, your cluster could be accessible to anyone. See https://www.elastic.co/guide/en/elasticsearch/reference/7.17/security-minimal-setup.html to enable security.
  if not es.ping():
Connected to Elasticsearch.
Loading preprocessed data...
Loaded 11000 records from data_with_ids.csv
Preparing data for bulk indexing...
Indexing documents...
/Users/nataliegavin/Desktop/CS 410/FINAL_PROJECT/elasticsearch/es_indexing.py:49: ElasticsearchWarning: Elasticsearch built-in security features are not enabled. Without authentication, your cluster could be accessible to anyone. See https://www.elastic.co/guide/en/elasticsearch/reference/7.17/security-minimal-setup.html to enable security.
  response = helpers.bulk(es, actions, raise_on_error=False, stats_only=False)
Documents indexed successfully.
Retrieving indexed documents with `_id`...
/Users/nataliegavin/Desktop/CS 410/FINAL_PROJECT/elasticsearch/es_indexing.py:61: ElasticsearchWarning: Elasticsearch built-in security features are not enabled. Without authentication, your cluster could be accessible to anyone. See https://www.elastic.co/guide/en/elasticsearch/reference/7.17/security-minimal-setup.html to enable security.
  for doc in helpers.scan(es, index="newsgroups"):
Saved indexed data with `_id` to 'data_with_ids.csv'.
es_indexing.py executed successfully.

Running es_search.py...
/Users/nataliegavin/Desktop/CS 410/FINAL_PROJECT/elasticsearch/es_search.py:27: ElasticsearchWarning: Elasticsearch built-in security features are not enabled. Without authentication, your cluster could be accessible to anyone. See https://www.elastic.co/guide/en/elasticsearch/reference/7.17/security-minimal-setup.html to enable security.
  response = es.search(index=index_name, body=query)
Score: 7.5192547, Text: science process modeling real world based commonly agreed interpretations observations perceptions v...

Score: 7.5192547, Text: science process modeling real world based commonly agreed interpretations observations perceptions v...

Score: 7.5192547, Text: science process modeling real world based commonly agreed interpretations observations perceptions v...

Score: 7.2849755, Text: let us explore interesting paragraph point point sentence sentence talking origins merely science or...

Score: 7.2849755, Text: let us explore interesting paragraph point point sentence sentence talking origins merely science or...

Score: 7.2849755, Text: let us explore interesting paragraph point point sentence sentence talking origins merely science or...

Score: 7.266502, Text: keep saying think means think means perhaps explain think science basis values means reason people s...

Score: 7.266502, Text: keep saying think means think means perhaps explain think science basis values means reason people s...

Score: 7.266502, Text: keep saying think means think means perhaps explain think science basis values means reason people s...

Score: 7.242238, Text: atoms objective arent even real scientists call atom nothing mathematical model describes certain ph...

es_search.py executed successfully.

Running clustering.py...
/Users/nataliegavin/Desktop/CS 410/FINAL_PROJECT/elasticsearch/clustering.py:42: ElasticsearchWarning: Elasticsearch built-in security features are not enabled. Without authentication, your cluster could be accessible to anyone. See https://www.elastic.co/guide/en/elasticsearch/reference/7.17/security-minimal-setup.html to enable security.
  helpers.bulk(es, actions)
Clustering complete and stored in Elasticsearch.
clustering.py executed successfully.

Running semantic_search.py...
Embeddings saved to 'embeddings.npy'
Top 5 Results for Query: 'science'

Score: 0.4487
Text: science progress via experimentation philosophising one aim experiments investigate validity hyptheses resulting models produced thinking process science one advantage approaches explaining world objective anything affects physical world studied example since part physical world anything including s...

Score: 0.4438
Text: living things maintain small electric fields enhance certain chemical reactions promote communication states cell communicate cells nervous system specialized example perhaps uses electric fields change location time large organism special photographic techniques applying external fields kirillian p...

Score: 0.4389
Text: living things maintain small electric fields enhance certain chemical reactions promote communication states cell communicate cells nervous system specialized example perhaps uses true electric fields change location time large organism also true special photographic techniques applying external fie...

Score: 0.4330
Text: making precisely one points wanted make fully agree big distinction process science end result end result science one wants get results objectively verifiable nothing objective process science good empirical research done showed merit homeopathic remedies would certainly valuable information would s...

Score: 0.4132
Text: scientific facts never heard thing science never proves disproves theory history tim

semantic_search.py executed successfully.

Running evaluation.py...
Evaluating Basic Search...
/Users/nataliegavin/Desktop/CS 410/FINAL_PROJECT/elasticsearch/evaluation.py:53: ElasticsearchWarning: Elasticsearch built-in security features are not enabled. Without authentication, your cluster could be accessible to anyone. See https://www.elastic.co/guide/en/elasticsearch/reference/7.17/security-minimal-setup.html to enable security.
  response = es.search(index=index_name, body=query_body)
Query: scientific advancements
Query: emerging technology trends
Basic Search - Precision@5: 0.2000, MRR: 0.7500

Evaluating Semantic Search...
Query: scientific advancements
Retrieved Docs (IDs): ['154', '5O8l1JIBZ_Hm77MkOLcO', '0O8l1JIBZ_Hm77Mk67mq', 'RgY0n5MB4Kdy6ZUdnrXE', '6O8l1JIBZ_Hm77Mk7cA0', '1976', 'YAY0n5MB4Kdy6ZUdoLxS', '10067', '_gY0n5MB4Kdy6ZUdpNvF', 'jO8l1JIBZ_Hm77Mk8eCV']
Cosine Scores: (0.49022650718688965, 0.49022650718688965, 0.49022650718688965, 0.49022650718688965, 0.47923743724823, 0.47923743724823, 0.47923743724823, 0.47425782680511475, 0.47425782680511475, 0.47425782680511475)
Relevant Found in Top-K (IDs): [0, 0, 0, 1, 0, 0, 1, 1, 0, 1]
Query: emerging technology trends
Retrieved Docs (IDs): ['988', 'hQY0n5MB4Kdy6ZUdn7i3', 'Ee8l1JIBZ_Hm77Mk7L1v']
Cosine Scores: (0.4515954852104187, 0.4515954852104187, 0.4515954852104187)
Relevant Found in Top-K (IDs): [0, 1, 0]
Semantic Search - Precision@10: 0.3667, MRR: 0.5589
evaluation.py executed successfully.