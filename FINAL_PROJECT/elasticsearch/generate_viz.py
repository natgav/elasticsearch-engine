# Import necessary libraries
# import pandas as pd
# import matplotlib.pyplot as plt
# from wordcloud import WordCloud

# # Load the data
# data = pd.read_csv("/Users/nataliegavin/Desktop/FINAL_PROJECT/preprocessed_data.csv")  # Adjust path if needed

# # Category Distribution
# # plt.figure(figsize=(10, 6))
# # data['target'].value_counts().plot(kind='bar')
# # plt.title("Category Distribution")
# # plt.xlabel("Category (Target)")
# # plt.ylabel("Number of Documents")
# # plt.savefig("category_distribution.png")  # Save as PNG file
# # plt.show()

# # Word Cloud
# plt.figure(figsize=(10, 6))
# plt.imshow(WordCloud, interpolation='bilinear')
# plt.axis("off")
# plt.title("Most Common Words in Processed Text")
# plt.savefig("word_cloud.png")  # Save as PNG file
# plt.show()
# from wordcloud import WordCloud
# import matplotlib.pyplot as plt
# import pandas as pd

# # Load the data
# data = pd.read_csv("/Users/nataliegavin/Desktop/FINAL_PROJECT/preprocessed_data.csv")  # Adjust path if needed

# # Generate word cloud
# all_text = ' '.join(data['processed_text'].dropna().tolist())  # Drop NaN values to avoid issues
# wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_text)

# # Display the word cloud
# plt.figure(figsize=(10, 6))
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis("off")
# plt.title("Most Common Words in Processed Text")
# plt.show()

import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("/Users/nataliegavin/Desktop/FINAL_PROJECT/preprocessed_data.csv")

#FOR showing processed data
#display first 5 rows of original and processed text
print(data[['text', 'processed_text']].head())


#dictionary mapping target numbers to category names
# category_names = {
#     0: "alt.atheism",
#     1: "comp.graphics",
#     2: "comp.os.ms-windows.misc",
#     3: "comp.sys.ibm.pc.hardware",
#     4: "comp.sys.mac.hardware",
#     5: "comp.windows.x",
#     6: "misc.forsale",
#     7: "rec.autos",
#     8: "rec.motorcycles",
#     9: "rec.sport.baseball",
#     10: "rec.sport.hockey",
#     11: "sci.crypt",
#     12: "sci.electronics",
#     13: "sci.med",
#     14: "sci.space",
#     15: "soc.religion.christian",
#     16: "talk.politics.guns",
#     17: "talk.politics.mideast",
#     18: "talk.politics.misc",
#     19: "talk.religion.misc"
# }

# map 'target' column to category names
# data['category_name'] = data['target'].map(category_names)

# generate the category distribution plot
# plt.figure(figsize=(12, 8))
# data['category_name'].value_counts().sort_index().plot(kind='bar', color='skyblue')
# plt.title("Category Distribution in 20 Newsgroups Dataset")
# plt.xlabel("Category")
# plt.ylabel("Number of Documents")
# plt.xticks(rotation=45, ha="right")
# plt.tight_layout()
# plt.savefig("cat_dist.png")
# plt.show()



