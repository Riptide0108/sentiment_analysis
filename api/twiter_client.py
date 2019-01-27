#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: riptide
"""

import re 
import tweepy 
import config as cfg
from tweepy import OAuthHandler 
import pandas as pd
import sys
sys.path.insert(0,'/home/riptide/Code/data_science/sentiment_analysis/api')
from SentimentAnalysis import SentimentAnalysis
from bs4 import BeautifulSoup

class TwitterClient(): 
    
    def __init__(self): 
        
        # keys and tokens from the Twitter Dev Console 
        consumer_key = cfg.CONSUMER_KEY
        consumer_secret = cfg.CONSUMER_SECRET
        access_token = cfg.ACCESS_TOKEN
        access_token_secret = cfg.ACCESS_SECRET
  
        # attempt authentication 
        try:
            
            # create OAuthHandler object 
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            
            # set access token and secret 
            self.auth.set_access_token(access_token, access_token_secret) 
            
            # create tweepy API object to fetch tweets 
            self.api = tweepy.API(self.auth) 
            
        except:
            
            # Set error vairable
            self.error = 'Authentication Failure'
  
    def clean_tweet(self,tweet): 
        
        # Remove RT (Retweet) from start of tweet
        tweet = re.sub('RT','',tweet)
        
        # Regex for @mention
        pat1 = r'@[A-Za-z0-9]+'
        
        # Regex for urls
        pat2 = r'https?://[A-Za-z0-9./]+'
        
        # Combine regex
        combined_pat = r'|'.join((pat1, pat2))
        
        # Beautifulsoup for HTML codings
        soup = BeautifulSoup(tweet, 'lxml')
        souped = soup.get_text()
        
        # Apply regex
        stripped = re.sub(combined_pat, '', souped)
        
        # utf8 encodings
        try:
            clean = stripped.decode("utf-8-sig").replace(u"\ufffd", "?")
        except:
            clean = stripped
            
        # remove hashtags and other special characters
        letters_only = re.sub("[^a-zA-Z]", " ", clean)
        
        # return clean tweet without trailing spaces
        return ("".join(letters_only)).strip() 
  
    def get_tweet_sentiment(self, tweets): 
        
        # Make object SentimentAnalysis
        sa = SentimentAnalysis()

        # clean tweets
        clean_tweets = tweets.apply(self.clean_tweet)
    
        # get sentiment 
        sentiment = sa.get_sentiment(clean_tweets)
        
        # convert to json format
        
        sentiment_json = {}
        for i in range(clean_tweets.shape[0]):
            sentiment_json[clean_tweets.iloc[i]] = sentiment[i]
        
        return sentiment_json
  
    def get_tweets(self, query, count = 10): 
        
        # empty series to store parsed tweets 
        tweets = pd.Series()
  
        try: 
            
            # call twitter api to fetch tweets 
            fetched_tweets = self.api.search(q = query, count = count, lang = 'en',tweet_mode='extended')
            
            # add text of each tweet in the series
            for tweet in fetched_tweets: 
                tweets.loc[tweets.shape[0]+1] = tweet.full_text
                
            return tweets 
            
        except tweepy.TweepError as e: 
            
            # return error (if any) 
            return str(e)
            