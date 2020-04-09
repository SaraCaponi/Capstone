from TweepyFunctions import get_users_tweets, get_hashtag_tweets
from AggregateFunction import aggregateData 
import json 
from datetime import datetime
from DatabaseQueries import cluster, db, collection 
import boto3

runtime = boto3.client(
    'sagemaker-runtime',
    aws_access_key_id='AKIASKF3S7J2ZW36FB7V',
    aws_secret_access_key='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',
    region_name='us-east-1'
    )

query = "ITryToAvoidPeopleWho"
#tweets = get_users_tweets(query)
tweets = get_hashtag_tweets(query)


if not tweets:
  print("no tweets avalible for given query")
else:
  response = runtime.invoke_endpoint(
      EndpointName='twitter-svc-tuner-200324-1449-015-0d842270',
      Body=json.dumps(tweets),
      ContentType='application/json')

  results = json.loads(response['Body'].read())

 # for pred in results['results']:
   #   print(pred)

  result = aggregateData(results)
  print(result)
 
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



