import unittest
from TweepyFunctions import get_users_tweets, get_hashtag_tweets, RATE_ERROR, SEARCH_ERROR
from AggregateFunction import aggregateData 
import json

tweets = {'tweet': ['Fresh pastry from Beetbox in the house!', 'Spent 2 days in New Orleans. Gained 75 lbs. Totally worth it.', "Here to give you dinner inspo, so you don't keep eating chips for dinner."]}
result = {'score': 0.42857142857142855, 'posIndex': 2 , 'negIndex': 4}

class TestTweepyFunctions(unittest.TestCase):

    def test_private_user(self):
        self.assertEqual(get_users_tweets("saracaponi14"), SEARCH_ERROR)

    def test_non_existing_user(self):
        self.assertEqual(get_users_tweets("ioh2389rh"), SEARCH_ERROR)

    def test_no_tweets_in_past_year(self):
        self.assertEqual(get_users_tweets("TestUse37457341"),[])
    
    def test_sucessful_username_search(self):
        self.assertEqual(get_users_tweets("TestUse39179756"),tweets)
    
    def test_empty_hashtag(self):
        self.assertEqual(get_hashtag_tweets("qwiowef0d"),[])
    
    # cannot test for specific tweets because tweepy only returns searched tweets within the last 7 days 
    # so the response would be ever changing
    def test_sucessful_hashtag_search(self):
        self.assertIsNot(get_hashtag_tweets("test"),[])
        self.assertIsNot(get_hashtag_tweets("test"),SEARCH_ERROR)

    def test_sucessful_aggregate(self):
        with open('Tweepy/TestData.json') as f:
            data = json.load(f)
        self.assertEqual(aggregateData(data), result)
        

if __name__ == '__main__':
    unittest.main()