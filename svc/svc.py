
import argparse
import json
import os
import re
from io import StringIO
from distutils.util import strtobool

import numpy as np
import pandas as pd

from sklearn.externals import joblib
# import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score

from sagemaker_containers.beta.framework import worker

import nltk
nltk.download('stopwords')

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
def preprocess(tweet, stem=False):
    """Preprocesses one tweet"""
    tweet = re.sub(TWEET_CLEANING_RE, ' ', str(tweet).lower()).strip()
    tokens = []
    for token in tweet.split():
        if token not in stop_words:
            if stem:
                tokens.append(stemmer.stem(token))
            else:
                tokens.append(token)
    return " ".join(tokens)


def model_fn(model_dir):
    clf = joblib.load(os.path.join(model_dir, 'model.joblib'))
    return clf


def input_fn(request_body, request_content_type):
    """An input_fun that loads JSON into a Pandas DataFrame, and preprocesses the tweets"""
    if request_content_type == "application/json":
        # TODO We don't really need Pandas here anymore
        df = pd.read_json(StringIO(request_body))
        # TODO Add way to provide stem parameter
        df.tweet = df.tweet.apply(lambda x: preprocess(x))
        return df['tweet'].to_numpy()
    else:
        raise ValueError(
            '{} is not supported by script.'.format(request_content_type))


def predict_fn(input_data, model):
    pred = model.predict(input_data)
    deci_func = model.decision_function(input_data)

    predictions = []
    for p, d in zip(pred, deci_func):
        predictions.append({
            'prediction': p,
            'probability': d
        })

    return {'results': predictions}


def output_fn(prediction, content_type):
    if content_type == 'application/json':
        return worker.Response(json.dumps(prediction), content_type, mimetype=content_type)
    else:
        raise ValueError(
            '{} accept type is not supported by this script.'.format(content_type))


if __name__ == '__main__':
    print('Extracting arguments')

    parser = argparse.ArgumentParser()

    # Hyperparameters from the client
    parser.add_argument('--stem', type=bool, default=False)
    parser.add_argument('--use-idf', type=str, default='true')
    parser.add_argument('--smooth-idf', type=str, default='true')
    parser.add_argument('--sublinear-tf', type=str, default='true')
    parser.add_argument('--C', type=float, default=1.0)
    parser.add_argument('--penalty', type=str, default='l2')
    parser.add_argument('--loss', type=str, default='squared_hinge')

    # Data, model, and output directories
    # TODO Remove this argument?
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

    print('Reading Tweets')
    train_df = pd.read_csv(os.path.join(args.train, args.train_file))
    test_df = pd.read_csv(os.path.join(args.test, args.test_file))

    print('Length of train_df: {}'.format(str(len(train_df.index))))
    print('Length of test_df: {}'.format(str(len(test_df.index))))

    print('Preprocessing the Tweets')
    # Decode Sentiment/Target
    train_df.target = train_df.target.apply(lambda x: decode_sentiment(x))
    test_df.target = test_df.target.apply(lambda x: decode_sentiment(x))

    # Preprocess Tweet
    train_df.tweet = train_df.tweet.apply(lambda x: preprocess(x, args.stem))
    test_df.tweet = test_df.tweet.apply(lambda x: preprocess(x, args.stem))

    print('Building training and testing datasets')
    X_train = train_df['tweet']
    y_train = train_df['target']
    X_test = test_df['tweet']
    y_test = test_df['target']

    # TODO TfIdf preprocessor?

    print('Training the model')
    pipe = Pipeline([
        ('tfidf', TfidfVectorizer(use_idf=bool(strtobool(args.use_idf)),
                                  smooth_idf=bool(strtobool(args.smooth_idf)),
                                  sublinear_tf=bool(strtobool(args.sublinear_tf)))),
        ('svc', LinearSVC(C=args.C,
                          penalty=args.penalty,
                          loss=args.loss))
    ])

    clf = pipe.fit(X_train, y_train)

    print('Print validation statistics')
    pred = clf.predict(X_test)
    # pred_prob = clf.predict_proba(X_test)
    decision = clf.decision_function(X_test)

    print(pred)
    print(decision)

    # TODO Why the fuck are these the same?
    print('Accuracy: {}'.format(accuracy_score(y_test, pred)))
    # print('Precision: {}'.format(precision_score(y_test, pred, average='macro')))
    # print('Recall: {}'.format(recall_score(y_test, pred, average='micro')))
    # TODO Add more validation statistics

    print('Save the model')
    joblib.dump(clf, os.path.join(args.model_dir, 'model.joblib'))
