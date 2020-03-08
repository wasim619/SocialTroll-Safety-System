from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
import pandas as pd
import os
import tweepy
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from textblob import Word
#from textblob.np_extractors import ConllExtractor
import sys
import requests
import json
# Create your views here.

consumer_key = 'MRHU43ElXTPiVXC0pfzlaXCbN'
consumer_secret = 'wX7nfU7ZZ3JamOJxMuqxViohxeYmE8gymrsne7Q1RJWPUSKNkk'
access_token = '1176344216189800448-dF9UQCDhRiiiY7nWhkc4hxvIOWFLwM'
access_token_secret = 'Aa9lexhNWXSAZoak7IBZYtvgbUIfVxZf5mYLOYjwTtZ4U'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if(request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        try:
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                # messages.success(
                #     request, ('Error - logging in - Please try again'))
                return redirect('login')
        except:
            return render(request, 'trollapp/login.html')
    else:
        return render(request, 'trollapp/login.html')


def dashboard(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.is_authenticated:

        data = pd.read_csv('data/dummydata.csv')
        x = data.groupby('polar').count()
        neg = x['date'][0]
        pos = x['date'][2]
        non = x['date'][1]
        #print(neg, pos, non)
        noOfPerson = data.groupby('date').count().shape[0]
        total = neg + pos + non

        mon = len(data[(data['date'] == '2019-01-10')])
        tue = len(data[(data['date'] == '2019-01-09')])
        wed = len(data[(data['date'] == '2019-01-07')])
        thur = len(data[(data['date'] == '2019-02-04')])
        fri = len(data[(data['date'] == '2019-02-22')])
        sat = len(data[(data['date'] == '2019-03-15')])
        sun = len(data[(data['date'] == '2019-03-25')])

        onemonth = [len(data[(data['date'] == '2019-01-01')]), len(data[(data['date'] == '2019-01-04')]), len(data[(data['date'] == '2019-01-07')]), len(data[(data['date'] == '2019-01-10')]), len(data[(data['date'] == '2019-01-13')]), len(data[(data['date']
                                                                                                                                                                                                                                                     == '2019-01-16')]), len(data[(data['date'] == '2019-01-19')]), len(data[(data['date'] == '2019-01-22')]), len(data[(data['date'] == '2019-01-25')]), len(data[(data['date'] == '2019-01-28')]), len(data[(data['date'] == '2019-01-31')])]
        # print(onemonth)

        monthvalue = ["2019-01-01", "2019-01-01", "2019-01-07", "2019-01-10", "2019-01-13",
                      "2019-01-16", "2019-01-19", "2019-01-22", "2019-01-25", "2019-01-28", "2019-01-31"]

        data = pd.read_csv('data/comments.csv')
        recentincidents = []

        for i in range(data.shape[0]):
            recentincidents.append(
                {"username": data['username'][i], "body": data['message'][i], "date": data['date'][i]})
        # print(recentincidents)
        chart1 = [22, 30, 17]
        chart2 = [78, 12, 44]

        contex = {'neg': neg, 'pos': pos, 'non': non, 'total': total, 'msg': noOfPerson,
                  'mon': mon, 'tue': tue, 'wed': wed, 'thur': thur, 'fri': fri, 'sat': sat, 'sun': sun, 'onemonth': onemonth, 'monthvalue': monthvalue, 'recentincidents': recentincidents, "chart1": chart1, "chart2": chart2}

    # recentincidents = [{"body": , "date": , "username": }]
        return render(request, 'trollapp/dashboard.html', contex)


def moderate(request):
    return render(request, 'trollapp/moderate.html')


def index(request):
    return render(request, 'trollapp/index.html')


def report(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        name = request.POST.get('PId')
        new_tweets = api.user_timeline(
            screen_name=request.POST['PId'], count=5)
        passedMessage = []
        bullyCount = 0
        nonBullyCount = 0
        users = []
        for tweet in new_tweets:
            analysis = TextBlob(tweet.text, analyzer=NaiveBayesAnalyzer())
            polarity = 'Positive'
            if (analysis.sentiment.p_pos < 0.55):
                polarity = 'Bully'
            elif((analysis.sentiment.p_pos > 0.56) and (analysis.sentiment.p_pos < 0.65)):
                polarity = 'none'
            else:
                polarity = 'Non Bully'
            # print(tweet.text)
            if(tweet.text[0] == 'R' and tweet.text[1] == 'T'):
                name = tweet.text.split('RT @')[1].split(":")[0]
            else:
                name = tweet.user.name
            message = tweet.text
            # print("Sentiment Analysis and Topic of Interest")
            # print("Tweet : ", tweet.text)
            # print("Sentiment:", polarity)
            # print("Confidence :  Positive score: ", analysis.sentiment.p_pos *
            #       100, "  Negative score: ", analysis.sentiment.p_neg*100)
            # print("Areas of interest: ", analysis.noun_phrases)
            passedMessage.append(
                {"name": name, "body": message, "type": polarity})
            if(polarity == 'Bully'):
                bullyCount += 1
            elif(polarity == 'Non Bully'):
                nonBullyCount += 1

            if(name not in users):
                users.append(name)

        if(bullyCount >= nonBullyCount):
            troll = 'Yes'
        else:
            troll = 'No'
        print(users)
        count = 0
        for i in request.POST['PId']:
            count = count + ord(i)

        data = {"submit": "block", "message": passedMessage,
                'troll': troll, 'user': '\n'.join(users), "count": count % 97, "name": name}
    else:
        data = {"submit": "none"}
    return render(request, 'trollapp/reports.html', data)


def logout_user(request):

    if not request.user.is_authenticated:
        return redirect('login')
    data = {"name": request.user.username}
    logout(request)
    return render(request, 'trollapp/logout.html', data)


def base(request):
    return render(request, 'trollapp/base.html')
