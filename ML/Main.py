# Daniel Jaegers
# Created on 2/2/2020

# DataFrame
import pandas as pd

# Plotting
import matplotlib.pyplot as plt

# Misc
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

# NLTK
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

# Loads of constants
DATASET_COLUMNS = ['target', 'ids', 'date', 'flag', 'user', 'text']
DATASET_ENCODING = 'ISO-8859-1'
TRAIN_SIZE = 0.8

TWEET_CLEANING_RE = "@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+"

decode_map = {
    0: 'NEGATIVE',
    2: 'NEUTRAL',
    4: 'POSITIVE'
}

# Read in Sentiment140
df = pd.read_csv('training.1600000.processed.noemoticon.csv', encoding = DATASET_ENCODING , names = DATASET_COLUMNS)
df = df.sample(frac = 0.1) 
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
# Scale the data to [-1, 1] in order to increase SVM speed
# scaling = MinMaxScaler(feature_range = (-1,1)).fit(X_train)
# X_train = scaling.transform(X_train)
# X_test = scaling.transform(X_test)

# -----------------------------------------------------------------------------------------
# Split the data into testing and training

df_train, df_test = train_test_split(df, test_size = 1 - TRAIN_SIZE, random_state = 69)
print('Length:\n\tData: {}\n\tTrain: {}\n\tTest: {}\n'.format(len(df), len(df_train), len(df_test)))

# -----------------------------------------------------------------------------------------
# Vectorize

vectorizer = TfidfVectorizer(min_df = 5,
    max_df = 0.8, sublinear_tf = True, use_idf = True)

train_vectors = vectorizer.fit_transform(df_train['text'])
test_vectors = vectorizer.fit_transform(df_test['text'])

print(test_vectors)
print(test_vectors.shape)

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
classifier_linear.fit(train_vectors, df_train['target'])
prediction_linear = classifier_linear.predict(test_vectors)

report = classification_report(df_test['target'], prediction_linear, output_dict = True)

print('positive: ', report['pos'])
print('negative: ', report['neg'])
