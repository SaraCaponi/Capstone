from TweepyFunctions import get_users_tweets, get_hashtag_tweets, RATE_ERROR, SEARCH_ERROR
from AggregateFunction import aggregateData 
import json 
from datetime import datetime
from DatabaseQueries import cluster, db, collection 
from Credentials import aws_access_key_id, aws_secret_access_key
import boto3

# connect to endpoint
runtime = boto3.client(
    'sagemaker-runtime',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name='us-east-1'
    )

# get the tweets
query = "nytimes"
#tweets = get_hashtag_tweets(query)
tweets = get_users_tweets(query)

#if rate limit was exceeded print message
if tweets == RATE_ERROR:
  print("Rate limit reached. Please wait before trying again")

#if search error occured print message
elif tweets == SEARCH_ERROR:
  print("no tweets avalible for given query")

# if sucessfully pulled tweets, send to alg
else:
  response = runtime.invoke_endpoint(
      EndpointName='twitter-svc-tuner-200324-1449-015-0d842270',
      Body=json.dumps(tweets),
      ContentType='application/json')

  # gets response from alg
  results = json.loads(response['Body'].read())

  #aggregates the results into a result object with score, posIndex, and negIndex
  result = aggregateData(results)
  #print(result)
 
  #creates database entry
  now = datetime.now()
  post = {"_id" : 5,
       "query": query,
        "type" : "hashtag",
        "score" : result['score'],
        "mostPositive" : tweets['tweet'][result['posIndex']],
        "mostNegative" : tweets['tweet'][result['negIndex']],
        "timeLog" : now
        }

  #comment this line out if you dont want to log the results in the database
  collection.insert_one(post)
