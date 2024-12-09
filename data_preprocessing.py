#2
#preprocessing data
import pandas as pd
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
nltk.download('punkt')
nltk.download('stopwords')

#initialize stop words
stop_words = set(stopwords.words('english'))

#load the dataset
data = pd.read_csv("newsgroups_data.csv")

def preprocess_text(text):
    #handle null
    if not isinstance(text, str):
        return ""
    
    #lowercase and remove non-alphabet characters
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    
    #tokenize and remove stop words
    tokens = [word for word in word_tokenize(text) if word not in stop_words]
    return " ".join(tokens)

#preprocessing
data['processed_text'] = data['text'].apply(preprocess_text)
data.to_csv("preprocessed_data.csv", index=False)  #also saved to csv for later use
print("Data preprocessing complete and saved to 'preprocessed_data.csv'.")


