import tweepy 
import json
from TweepyCredentials import auth
from datetime import datetime 
from datetime import timedelta


def get_users_tweets(username): 

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True) 

    # gets the current time and subtracts 1 year to find the end time
    current_time = datetime.now()
    end_time = current_time - timedelta(days=365)

    temp = []
    # attempts to get users tweets, if user does not exist or api call fails will return empty array 
    try:
         # gets first 200 tweets
        tweets = api.user_timeline(screen_name=username, 
                                   count = 200,
                                   tweet_mode="extended"
                                   ) 
        # creates array to hold all of the tweets and appends the exsiting tweets array to it
        all_tweets = []
        all_tweets.extend(tweets)
        # gets the id of the last tweet 
        oldest_id = tweets[-1].id

        # while the time of tweet of the last tweet in the array is more than the end time
        while tweets[-1].created_at > end_time:
            # gets the next 200 tweets starting at the last id
            tweets = api.user_timeline(screen_name=username, 
                           count=200,
                           max_id = oldest_id - 1, 
                           tweet_mode="extended"
                           )
            # if there are no more tweets, break the loop 
            if len(tweets) == 0:
                break
            # sets the oldest_id to the id of the last tweet    
            oldest_id = tweets[-1].id
            # adds the tweets to the all_tweets array
            all_tweets.extend(tweets)
            
    # if there was an error in pulling the tweets return an empty array 
    except tweepy.TweepError:
        return []
    
    for tweet in all_tweets:
        # need to do another check because the code could enter the loop but only 5 more tweets were in the last year
        if tweet.created_at > end_time:
            # extracts just the text
            temp.append(tweet.full_text)
    
    # returns array of tweets if sucessful, empty array if error
    return temp
    


def get_hashtag_tweets(hashtag):

    tweets = []
    # create api call 
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True) 
    try:
        #gets 100 tweets at a time until there are 3200 total
        for tweet in tweepy.Cursor(api.search,q="#"+hashtag,
                               count=100,
                               lang="en",
                               tweet_mode="extended"
                               ).items(3200):
            #appends the tweets to the arry 
            tweets.append(tweet.full_text)
    
      # returns array of tweets if sucessful, empty array if error
    except tweepy.TweepError:
        return []
    return tweets 
