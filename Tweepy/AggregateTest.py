from TweepyFunctions import get_users_tweets, get_hashtag_tweets
from AggregateFunction import aggregateData 
import json 
from datetime import datetime
from DatabaseSetup import cluster, db, collection 

query = "mizzou"
tweets = get_users_tweets(query)


# pass to sentiment alg
# run aggregateData with result from sentiment algorothm 
# using TestData.json for now
with open('/Users/saracaponi/Desktop/Capstone/Code/TestData.json') as f:
  data = json.load(f)
  result = aggregateData(data)

now = datetime.now()
post = {"_id" : ,
       "query": query,
        "type" : "user",
        "score" : result['score'],
        "mostPositive" : tweets[result['posIndex']],
        "mostNegative" : tweets[result['negIndex']],
        "timeLog" : now
        }

collection.insert_one(test)



