from flask import render_template, flash, redirect
from app import application
from app.forms import SearchForm
from .TweepyFunctions import *
from .Credentials import *
import pymongo
from pymongo import MongoClient
import json 
import boto3
from datetime import datetime

@application.route('/', methods=['GET', 'POST'])
@application.route('/index/', methods=['GET', 'POST'])
def home():
    form = SearchForm()

    if form.validate_on_submit():
        flash('Query {}'.format(form.query.data))

        runtime = boto3.client(
        'sagemaker-runtime',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name='us-east-1'
        )

        # get tweets
        if(form.submitUsername.data):
            search_type = 'user'
            tweets = get_users_tweets(form.query.data)
        else:
            search_type = 'hashtag'
            tweets = get_hashtag_tweets(form.query.data)

        #if rate limit was exceeded print message
        if tweets == RATE_ERROR:
            print("Rate limit reached. Please wait before trying again")

        #if search error occured print message
        elif tweets == SEARCH_ERROR:
            print("The username searched is either private or does not exist")

        #if no tweets exist
        elif not tweets:
            print("There are no avalible tweets for that user or hashtag")

        else:
            processedTweets = []
            #send each tweet to preprocess function
            for x in tweets['tweet']:
                processedTweets.append(preprocess(x))

            processedTweet = {"tweet": processedTweets}
      
            #call sentiment alg with processedTweet
            response = runtime.invoke_endpoint(
            EndpointName='twitter-svc-tuner-200324-1449-015-0d842270',
            Body=json.dumps(processedTweet),
            ContentType='application/json')

            results = json.loads(response['Body'].read())

            #aggregates the results into a result object with score, posIndex, and negIndex
            result = aggregateData(results)

             #creates database entry
            now = datetime.now()
            post = {
                "query": form.query.data,
                "type" : search_type,
                "score" : result['score'],
                "mostPositive" : tweets['tweet'][result['posIndex']],
                "mostNegative" : tweets['tweet'][result['negIndex']],
                "timeLog" : now
             }
            cluster = MongoClient(database_connect)
            db = cluster["DSS"]
            collection = db["Search_Records"]
            #comment this line out if you dont want to log the results in the database
            collection.insert_one(post)

        # Use flash messages to display validation errors and stuff
            return render_template('index.html',
                                 form=form, 
                                 data=form.query.data, 
                                 score=result['score'], 
                                 posTweet = tweets['tweet'][result['posIndex']],
                                 negTweet =tweets['tweet'][result['negIndex']]
                                 )


    return render_template('index.html', form=form)

@application.route('/username/')
def username():
    return render_template('username.html')

@application.route('/hashtag/')
def hashtag():
    return render_template('hashtag.html')

@application.route('/about/')
def about():
    return render_template('about.html')