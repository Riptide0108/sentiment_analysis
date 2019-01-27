#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 11:30:38 2019

@author: riptide
"""
from flask import request, json
from api import app

import sys
sys.path.insert(0,'/home/riptide/Code/data_science/sentiment_analysis/api')

from twiter_client import TwitterClient




@app.route('/')
@app.route('/index')
def index():
    return "Sentiment Analysis API"

@app.route('/get_sentiment',methods = ['POST'])
def get_sentiment():
    if request.method == 'POST':
        query = request.form.get('query')
        count = request.form.get('count')
        
        tc = TwitterClient()
        
        tweets = tc.get_tweets(query,count)

        print(type(tweets))
        
        sentiment = tc.get_tweet_sentiment(tweets)
        
        response = app.response_class(
                response=json.dumps(sentiment),
                status=200,
                mimetype='application/json'
                )   
    return response
        
        