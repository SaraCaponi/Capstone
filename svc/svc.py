import argparse
import os
import re
from io import StringIO

import numpy as np
import pandas as pd

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score

from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

stop_words = stopwords.words("english")
stemmer = SnowballStemmer("english")

TWEET_CLEANING_RE = r'@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+'

decode_map = {
    0: 'NEGATIVE',
    2: 'NEUTRAL',
    4: 'POSITIVE'
}


# Do I need this?
def decode_sentiment(label):
    return decode_map[int(label)]


# Adjust preprocessor to be better
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


def model_fn(model_dir):
    clf = joblib.load(os.path.join(model_dir, "model.joblib"))
    return clf


# What is my input format?
def input_fn(request_body, request_content_type):
    """An input_fun tat loads a pickled numpy array"""
    if request_content_type == "application/python-pickle":
        array = np.load(StringIO(request_body))
        return array
    else:
        # TODO Handle other content-types here or raise an Exception if the content type is not supported
        pass


def predict_fn(input_data, model):
    prediction = model.predict(input_data)
    # TODO Definitely need preprocessing
    pred_prob = model.predict_proba(input_data)
    return np.array([prediction, pred_prob])


def output_fn(prediction, content_type):
    # TODO Implement output_fn
    pass


if __name__ == '__main__':
    print('Extracting arguments')

    parser = argparse.ArgumentParser()

    # Hyperparameters from the client
    parser.add_argument('--stem', type=bool, default=False)
    parser.add_argument('--use-idf', type=bool, default=True)
    parser.add_argument('--smooth-idf', type=bool, default=True)
    parser.add_argument('--sublinear-tf', type=bool, default=True)
    parser.add_argument('--kernel', type=str, default='linear')
    parser.add_argument('--C', type=float, default=1.0)

    # Data, model, and output directories
    # parser.add_argument('--output-data-dir', type=str,
    #                     default=os.environ.get('SM_OUTPUT_DATA_DIR'))
    parser.add_argument('--model-dir', type=str,
                        default=os.environ.get('SM_MODEL_DIR'))
    parser.add_argument('--train', type=str,
                        default=os.environ.get('SM_CHANNEL_TRAIN'))
    parser.add_argument('--test', type=str,
                        default=os.environ.get('SM_CHANNEL_TEST'))
    parser.add_argument('--train-file', type=str, default='twitter_train.csv')
    parser.add_argument('--test-file', type=str, default='twitter_test.csv')

    args, _ = parser.parse_known_args()

    # Load from args.train and args.test, train a model, write model to args.model_dir

    print('Reading Tweets')
    train_df = pd.read_csv(os.path.join(args.train, args.train_file))
    test_df = pd.read_csv(os.path.join(args.test, args.test_file))

    print('Preprocessing the Tweets')
    # Decode Sentiment/Target
    train_df.target = train_df.target.apply(lambda x: decode_sentiment(x))
    test_df.target = test_df.target.apply(lambda x: decode_sentiment(x))

    # Preprocess Tweet
    train_df.text = train_df.text.apply(lambda x: preprocess(x, args.stem))
    test_df.text = test_df.text.apply(lambda x: preprocess(x, args.stem))

    print('Building training and testing datasets')
    X_train = train_df['text']
    y_train = train_df['target']
    X_test = test_df['text']
    y_test = test_df['target']

    # print(X_train.head())
    # print(y_train.head())

    # TODO TfIdf preprocessor?

    print('Training the model')
    pipe = Pipeline([
        ('tfidf', TfidfVectorizer(use_idf=args.use_idf,
                                  smooth_idf=args.smooth_idf,
                                  sublinear_tf=args.sublinear_tf)),
        ('clf', SVC(kernel=args.kernel,
                    C=args.C))
    ])

    clf = pipe.fit(X_train, y_train)

    print('Print validation statistics')
    predicted = clf.predict(X_test)

    # TODO WHy the fuck are these the same?
    print('Accuracy: {}'.format(accuracy_score(y_test, predicted)))
    print('Precision: {}'.format(precision_score(
        y_test, predicted, average='macro')))
    print('Recall: {}'.format(recall_score(y_test, predicted, average='micro')))
    # TODO Add more validation statistics

    print('Save the model')
    joblib.dump(clf, os.path.join(args.model_dir, 'model.joblib'))
