#1
#loading in the dataset
from sklearn.datasets import fetch_20newsgroups
import pandas as pd
import matplotlib.pyplot as plt

#load the dataset
newsgroups = fetch_20newsgroups(subset='train', remove=('headers', 'footers', 'quotes'))
data = pd.DataFrame({'text': newsgroups.data, 'target': newsgroups.target})

#basic stats and class distribution
print("Dataset loaded successfully.")
print(f"Total documents: {len(data)}")
print("Target class distribution:\n", data['target'].value_counts())

#save original data to CSV for later use
data.to_csv("newsgroups_data.csv", index=False)
