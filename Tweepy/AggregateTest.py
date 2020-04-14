import json 
import boto3
from TweepyFunctions import *
from datetime import datetime
from DatabaseQueries import cluster, db, collection 
from Credentials import aws_access_key_id, aws_secret_access_key

# connect to endpoint
runtime = boto3.client(
    'sagemaker-runtime',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name='us-east-1'
    )

# get the tweets
query = "jimmyfallon"
#tweets = get_hashtag_tweets(query)
tweets = get_users_tweets(query)

#if rate limit was exceeded print message
if tweets == RATE_ERROR:
  print("Rate limit reached. Please wait before trying again")

#if search error occured print message
elif tweets == SEARCH_ERROR:
  print("The username searched is either private or does not exist")
  # or hashtag/username searched had invlid syntax

#if no tweets exist
elif not tweets:
  print("There are no avalible tweets for that user or hashtag")

# if sucessfully pulled tweets, run preprocessing algorithm 
else:
  processedTweets = []
  #send each tweet to preprocess function
  for x in tweets['tweet']:
    processedTweets.append(preprocess(x))

  #create new processedTweet obj and set its tweet value to processedTweets 
  processedTweet = {"tweet": processedTweets}
      
  #call sentiment alg with processedTweet
  response = runtime.invoke_endpoint(
      EndpointName='twitter-svc-tuner-200324-1449-015-0d842270',
      Body=json.dumps(processedTweet),
      ContentType='application/json')

  # gets response from alg
  results = json.loads(response['Body'].read())

  #aggregates the results into a result object with score, posIndex, and negIndex
  result = aggregateData(results)
  print(result)

  #creates database entry
  now = datetime.now()
  post = {
       "query": query,
        "type" : "user",
        "score" : result['score'],
        "mostPositive" : tweets['tweet'][result['posIndex']],
        "mostNegative" : tweets['tweet'][result['negIndex']],
        "timeLog" : now
        }

  #comment this line out if you dont want to log the results in the database
  collection.insert_one(post)
  
