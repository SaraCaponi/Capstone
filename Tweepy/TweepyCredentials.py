import tweepy 

consumer_key = "XXXX" 
consumer_secret = "XXXX"
access_key = "XXXX"
access_secret = "XXXX"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
  
# Access to user's access key and access secret 
auth.set_access_token(access_key, access_secret) 
  
