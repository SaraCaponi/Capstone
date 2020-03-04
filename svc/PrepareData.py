import boto3
import sagemaker

import pandas as pd

from sklearn.model_selection import train_test_split

# Loads of constants
DATASET_COLUMNS = ['target', 'ids', 'date', 'flag', 'user', 'text']
DATASET_ENCODING = 'ISO-8859-1'
TRAIN_SIZE = 0.8

# SageMaker Python SDK
sm_boto3 = boto3.client('sagemaker')
sess = sagemaker.Session()
region = sess.boto_session.region_name
bucket = sess.default_bucket()
print('Using bucket ' + bucket)

# Read the data locally
df = pd.read_csv('training.1600000.processed.noemoticon.csv',
                 encoding=DATASET_ENCODING, names=DATASET_COLUMNS)

# TODO This is bad, do better
df = df.sample(frac=0.02)

# TODO Ensure an even split of pos/neg?
X_train, X_test, y_train, y_test = train_test_split(
    df['text'], df['target'], test_size=1 - TRAIN_SIZE, random_state=69)

trainX = pd.DataFrame(X_train, columns=['text'])
trainX['target'] = y_train

testX = pd.DataFrame(X_test, columns=['text'])
testX['target'] = y_test

# Save the train_test_split locally
trainX.to_csv('twitter_train.csv', index=False)
testX.to_csv('twitter_test.csv', index=False)

# Send data to S3. SageMaker will take training data from S3
trainpath = sess.upload_data(
    path='twitter_train.csv', bucket=bucket,
    key_prefix='data/twitter')

testpath = sess.upload_data(
    path='twitter_test.csv', bucket=bucket,
    key_prefix='data/twitter')

print(trainpath)
print(testpath)
