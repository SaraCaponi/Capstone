# Daniel Jaegers
# Created on 2/2/2020

# TODO Move all of this into a notebook rather than a script!

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
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer, HashingVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline

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
df = pd.read_csv('ML/data/training.1600000.processed.noemoticon.csv',
                 encoding=DATASET_ENCODING, names=DATASET_COLUMNS)

# TODO Ensure that pos/neg ratio is 1:1
# The only reason that I am doing this is because my computer can't handle the full dataset
df = df.sample(frac=0.01)
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

# TODO Adjust preprocessor to be better
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


# -----------------------------------------------------------------------------------
# Pipeline

X_train, X_test, y_train, y_test = train_test_split(
    df['text'], df['target'], test_size=1 - TRAIN_SIZE, random_state=69)

pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', SVC())
])

# TODO TfIdf preprocessor step?

param_grid = [
    {
        'tfidf__use_idf': [True, False],
        'tfidf__smooth_idf': [True, False],
        'tfidf__sublinear_tf': [True, False],
        'clf__kernel': ['linear'],
        'clf__C': [x * 0.1 for x in range(1, 20)]
    },
    # {
    #     'clf__kernel': ['poly'],
    #     'clf__C': [x * 0.1 for x in range(1, 20)],
    #     'clf__gamma': ['scale', 'auto'],
    #     'clf__degree': [2, 3, 4, 5]
    # }
]


grid = GridSearchCV(pipeline, cv=3, param_grid=param_grid)
grid.fit(X_train, y_train)

# summarize results
print("Best: %f using %s" % (grid.best_score_,
                             grid.best_params_))
means = grid.cv_results_['mean_test_score']
stds = grid.cv_results_['std_test_score']
params = grid.cv_results_['params']
for mean, stdev, param in zip(means, stds, params):
    print("%f (%f) with: %r" % (mean, stdev, param))


# -----------------------------------------------------------------------------------------
# Vectorize

# vectorizer = TfidfVectorizer(sublinear_tf = True, use_idf = True)
# X = vectorizer.fit_transform(df['text']).toarray()

# -----------------------------------------------------------------------------------------
# Split the data into testing and training

# X_train, X_test, y_train, y_test = train_test_split(X, df['target'], test_size = 1 - TRAIN_SIZE, random_state = 69)
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

# classifier_linear = SVC(kernel = 'linear')
# classifier_linear.fit(X_train, y_train)
# prediction_linear = classifier_linear.predict(X_test)

# report = classification_report(y_test, prediction_linear, output_dict = True)
# print(json.dumps(report, indent = 2))


# cm = confusion_matrix(y_test, prediction_linear)
# print(cm)


# import seaborn as sns
# import matplotlib.pyplot as plt

# ax= plt.subplot()
# sns.heatmap(cm, annot = True, ax = ax, fmt = 'g') #annot = True to annotate cells

# # labels, title and ticks
# ax.set_xlabel('Predicted labels')
# ax.set_ylabel('True labels')
# ax.set_title('Confusion Matrix')
# ax.xaxis.set_ticklabels(['business', 'health'])
# ax.yaxis.set_ticklabels(['health', 'business'])
# plt.show()
