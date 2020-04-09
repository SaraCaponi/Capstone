import pymongo
from pymongo import MongoClient
from datetime import datetime 
from Credentials import database_connect

cluster = MongoClient(database_connect)
db = cluster["DSS"]
collection = db["Search_Records"]


#---------------------how to insert search query into database-------------------------

#now = datetime.now()
#test = {"_id" : ,
#       "query": query,
#        "type" : "user/hashtag",
#        "score" : result['score'],
#        "mostPositive" : tweets[result['posIndex']],
#        "mostNegative" : tweets[result['negIndex']],
#        "timeLog" : now
#        }

#collection.insert_one(test)



#--------------Leaderboard schema ---------------------------------------------------
#queries 10 most postive usernames for leaderboards
mostPosUser = collection.find({"type":"user"}).sort("score", -1).limit(10).distinct("query")

#queries 10 most negative usernames for leaderboard
mostNegUser = collection.find({"type":"user"}).sort("score", 1).limit(10).distinct("query")

#queries 10 most postive hashtags for leaderboard
mostPosHash = collection.find({"type":"hashtag"}).sort("score", -1).limit(10).distinct("query")

#queries 10 most negative hashtags for leaderboard
mostNegHash = collection.find({"type":"hashtag"}).sort("score", 1).limit(10).distinct("query")


#queries 10 most frequently searched hashtags 
result = collection.aggregate([
    # Match the type to be hashtag
    { "$match": { "type":"hashtag" } },

    # Group the documents with the same query and count them
    { "$group": {
        "_id": {
            "query": "$query"
        },
        "count": { "$sum": 1 }
    }},
    # sort the documents by most frequent
    { "$sort": {
        "_id.query": 1,
        "count": -1
        }
    },
    #group on query with $first to pick the document with most occurrences.
    { "$group": {
      "_id": {
        "query": "$_id.query"
      },
      "count": {
        "$first": "$count"
      }
    }
  },
  { "$limit" : 10 }
])
# pulls out just the queries from the aggregate response
mostFrequentHash = []
for x in result:
        mostFrequentHash.append(x["_id"]["query"])


#queries 10 most frequently searched usernames
result = collection.aggregate([
    # Match the type to be user
    { "$match": { "type":"user" } },

    # Group the documents with the same query and count them
    { "$group": {
        "_id": {
            "query": "$query"
        },
        "count": { "$sum": 1 }
    }},
    # sort the documents by most frequent
    { "$sort": {
        "_id.query": 1,
        "count": -1
        }
    },
    #group on query with $first to pick the document with most occurrences.
    { "$group": {
      "_id": {
        "query": "$_id.query"
      },
      "count": {
        "$first": "$count"
      }
    }
  },
  { "$limit" : 10 }
])
# pulls out just the queries from the aggregate response
mostFrequentUser = []
for x in result:
        mostFrequentUser.append(x["_id"]["query"])


now = datetime.now()
# schema for leaderboard creation
post = {"_id": 0,
         "postiveUser" : mostPosUser,
         "negativeUser" : mostNegUser,
         "frequencyUser" : mostFrequentUser,
         "postiveHash" : mostPosHash,
         "negativeHash" : mostNegHash,
         "frequencyHash" : mostFrequentHash,
         "timeCreated" : now     
}
#LBcollection = db["Leaderboard_Cache"]
#LBcollection.insert_one(post)
