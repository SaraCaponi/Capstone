import json

# to get score:
# need to add up all the positive tweets 
# add up all the negative tweets 
# subtract the negative tweets from the positive 
# divide by total number of tweets 



def aggregateData(data):
    # declaring and initializing return varaible 
    result = {'score': 0, 'posIndex': 0 , 'negIndex': 0}

    pos = 0
    neg = 0
    numOfTweets = 0
    
    # loops through the results array in the json response
    for x in data['results']:   
        numOfTweets += 1            # counts the number of tweets
        if x['prediction'] == "POSITIVE":   
            pos +=1          # counts the number of tweets that have a positive prediction
        else: 
            neg += 1        # counts the number of tweets with a negativee prediction 
    score = (pos - neg) /numOfTweets     # calculates the score 

    # sets the score of the result
    result['score'] = score

    mostNeg = 0
    mostPos = 0
    index = 0

    for x in data['results']:
        if x['probability'] > mostPos:   # if the probability for positive is greater than the current mosPos 
            mostPos = x['probability']   # set mostPos to current probablity 
            mostPosIndex = index            # sets the index
        if x['probability'] < mostNeg:   # if the probability for negative is greater than the current mostNeg 
            mostNeg = x['probability']   # set mostNeg to current probability 
            mostNegIndex = index            # sets the index
        index += 1                      # increments the index 

    # sets the results posIndex and negIndex values 
    result['posIndex'] = mostPosIndex
    result['negIndex'] = mostNegIndex

    return result

