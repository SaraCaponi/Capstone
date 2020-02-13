# Daniel Jaegers
# Created on 2/2/2020

# DataFrame
import pandas as pd

# Plotting
import matplotlib.pyplot as plt

# Misc
import json
import re
import time
from collections import Counter

# Scikit-learn
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn import svm
from sklearn.metrics import classification_report
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import confusion_matrix

# NLTK
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

# Loads of constants
DATASET_COLUMNS = ['target', 'ids', 'date', 'flag', 'user', 'text']
DATASET_ENCODING = 'ISO-8859-1'
TRAIN_SIZE = 0.8

TWEET_CLEANING_RE = r'@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+'

decode_map = {
    0: 'NEGATIVE',
    2: 'NEUTRAL',
    4: 'POSITIVE'
}

# Read in Sentiment140
# https://www.kaggle.com/kazanova/sentiment140
df = pd.read_csv('ML/training.1600000.processed.noemoticon.csv', encoding = DATASET_ENCODING , names = DATASET_COLUMNS)
df = df.sample(frac = 0.002) 
print(df.head())
print(df.dtypes)

# ------------------------------------------------------------------------------------
# Map the target integer to a category

def decode_sentiment(label):
    return decode_map[int(label)]

df.target = df.target.apply(lambda x: decode_sentiment(x))
print(df.head())
print(df.target.unique())

# --------------------------------------------------------------------------------------
# Plot the distribution of Sentiment140

# target_cnt = Counter(df.target)
# plt.figure(figsize=(16,8))
# plt.bar(target_cnt.keys(), target_cnt.values())
# plt.title('Sentiment140 Distribution')
# plt.show()

# ----------------------------------------------------------------------------------------
# Preprocess each tweet

stop_words = stopwords.words("english")
stemmer = SnowballStemmer("english")

def preprocess(text, stem=False):
    text = re.sub(TWEET_CLEANING_RE, ' ', str(text).lower()).strip()
    tokens = []
    for token in text.split():
        if token not in stop_words:
            if stem:
                tokens.append(stemmer.stem(token))
            else:
                tokens.append(token)
    return " ".join(tokens)

df.text = df.text.apply(lambda x: preprocess(x))
print(df.head())

# -----------------------------------------------------------------------------------------
# Vectorize

vectorizer = TfidfVectorizer(sublinear_tf = True, use_idf = True)
X = vectorizer.fit_transform(df['text']).toarray()

# -----------------------------------------------------------------------------------------
# Split the data into testing and training

X_train, X_test, y_train, y_test = train_test_split(X, df['target'], test_size = 1 - TRAIN_SIZE, random_state = 69)
# print('Length:\n\tData: {}\n\tTrain: {}\n\tTest: {}\n'.format(len(df), len(df_train), len(df_test)))

# -----------------------------------------------------------------------------------------
# Vectorize

# vectorizer = TfidfVectorizer(sublinear_tf = True, use_idf = True)

# train_vectors = vectorizer.fit_transform(df_train['text'])
# test_vectors = vectorizer.fit_transform(df_test['text'])

# print(test_vectors)
# print(test_vectors.shape)

# ---------------------------------------------
# Hash THEN vectorize 

# vectorizer = HashingVectorizer(verbose=True)
# train_vectors = vectorizer.fit_transform(df_train['text'])
# test_vectors = vectorizer.fit_transform(df_test['text'])

# print(test_vectors)
# print(test_vectors.shape)


# ----------------------------------------------------------------------------------------
# Create a linear SVM model

classifier_linear = svm.SVC(kernel = 'linear')
classifier_linear.fit(X_train, y_train)
prediction_linear = classifier_linear.predict(X_test)

report = classification_report(y_test, prediction_linear, output_dict = True)
print(json.dumps(report, indent = 2))


cm = confusion_matrix(y_test, prediction_linear)
print(cm)


import seaborn as sns
import matplotlib.pyplot as plt     

ax= plt.subplot()
sns.heatmap(cm, annot = True, ax = ax, fmt = 'g') #annot = True to annotate cells

# labels, title and ticks
ax.set_xlabel('Predicted labels')
ax.set_ylabel('True labels')
ax.set_title('Confusion Matrix')
ax.xaxis.set_ticklabels(['business', 'health']) 
ax.yaxis.set_ticklabels(['health', 'business'])
plt.show()