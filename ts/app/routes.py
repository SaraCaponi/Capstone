from flask import render_template, flash, redirect, send_from_directory
from app import application
from app.forms import SearchForm
from .TweepyFunctions import *
from .Credentials import *
import pymongo
from pymongo import MongoClient
import json
import boto3
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os

cluster = MongoClient(database_connect)
db = cluster["DSS"]
collection = db["Search_Records"]
LBcollection = db["Leaderboard_Cache"]


@application.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(application.root_path, 'static'),'favicon.ico',mimetype='image/vnd.microsof.icon')


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
            search_t = '@'
            tweets = get_users_tweets(form.query.data)
        else:
            search_type = 'hashtag'
            search_t = '#'
            tweets = get_hashtag_tweets(form.query.data)

        #if rate limit was exceeded print message
        if tweets == RATE_ERROR:
            return render_template('index.html',
                                 form=form,
                                 error= 'Rate limit reached. Please wait before trying again'
                                 )

        #if search error occured print message
        elif tweets == SEARCH_ERROR:
            return render_template('index.html',
                                 form=form,
                                 error= 'An error occured while searching. Please check that your syntax is correct or that the username searched exists and is not private.'
                                 )

        #if no tweets exist
        elif not tweets:
            return render_template('index.html',
                                 form=form,
                                 error= 'There are no avalible tweets for that user or hashtag'
                                 )

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

            #comment this line out if you dont want to log the results in the database
            collection.insert_one(post)

            #donut chart creation
            # create data
            names='Positive', 'Negative',
            size=[result['positive'],result['negative']]

            # Create a circle for the center of the plot
            # change color to = color of background to give illusion of transparency
            my_circle=plt.Circle( (0,0), 0.7, color='white', linewidth = 1, ls = '-', ec = 'white' )

            # Give color names and set wedge properites
            plt.pie(size, labels = names, labeldistance=1.1, colors=['skyblue','#0084b4'], wedgeprops = { 'linewidth' : 4, 'edgecolor' : 'white' })
            p=plt.gcf()
            p.gca().add_artist(my_circle)

            # needed to send chart as png to html page
            img = BytesIO()
            plt.savefig(img, format='png', transparent=True)
            plt.close()
            img.seek(0)
            donut_url = base64.b64encode(img.getvalue()).decode('utf8')

            new_score = (result['score'] + 1) * 100 / 2
            new_score = round(new_score, 1)

            # Use flash messages to display validation errors and stuff
            return render_template('index.html',
                                 form=form,
                                 data=form.query.data,
                                 search_type = search_t,
                                 score=new_score,
                                 posTweet = tweets['tweet'][result['posIndex']],
                                 negTweet =tweets['tweet'][result['negIndex']],
                                 donut_url='data:image/png;base64,'+ donut_url
                                 )


    return render_template('index.html', form=form)

@application.route('/username/')
def username():
    now = datetime.now()
    yesterday= now - timedelta(days=1)

    #get most recent leaderboard
    leaderboard = list(LBcollection.find().sort("timeCreated", -1).limit(1))

    # if the leaderboard was created in the last 24 hours
    if leaderboard[0]['timeCreated'] > yesterday:
        # render user leaderboards with existing leaderboard data
        return render_template('username.html',
                                mostPos=leaderboard[0]['postiveUser'],
                                mostNeg=leaderboard[0]['negativeUser'],
                                mostFreq = leaderboard[0]['frequencyUser']
                            )
    # if the most recent leaderboar is out dated
    else:
        # create a new leaderbord
        leaderboard = get_leaderboard()
        # render with new leaderboard data
        return render_template('username.html',
                                 mostPos=leaderboard['postiveUser'],
                                 mostNeg=leaderboard['negativeUser'],
                                 mostFreq = leaderboard['frequencyUser']
                                 )


    return render_template('username.html')

@application.route('/hashtag/')
def hashtag():
    now = datetime.now()
    yesterday= now - timedelta(days=1)

    # get the latest leaderboard in the database
    leaderboard = list(LBcollection.find().sort("timeCreated", -1).limit(1))

    # if the most recent leaderboard was created less than 24 hours ago
    if leaderboard[0]['timeCreated'] > yesterday:
        #render hashtag leaderboards with exisitng leaderboard
        return render_template('hashtag.html',
                                mostPos=leaderboard[0]['postiveHash'],
                                mostNeg=leaderboard[0]['negativeHash'],
                                mostFreq = leaderboard[0]['frequencyHash']
                            )

    # if the most recent leaderboard is outdated
    else:
        #create a new leaderboard
        leaderboard = get_leaderboard()
        # render using new leaderboard data
        return render_template('hashtag.html.html',
                                 mostPos=leaderboard['postiveHash'],
                                 mostNeg=leaderboard['negativeHash'],
                                 mostFreq = leaderboard['frequencyHash']
                                 )
    return render_template('hashtag.html')

@application.route('/about/')
def about():
    return render_template('about.html')
