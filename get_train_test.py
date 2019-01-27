#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 01:29:19 2019

@author: riptide
"""
# Necessary Imports
import os
import pandas as pd
import re
from sklearn.model_selection import train_test_split

# Change working directory
os.chdir('/home/riptide/Code/data_science/sentiment_analysis')

# Read data
data = pd.read_csv('data/data.csv', 
                   encoding = 'latin-1', 
                   header = None,
                   index_col = False)
data.columns = ['sentiment','id','time','query','username','tweet']

# Sample 5% of data (to memory issues during tokenization)
data = data.sample(frac = 0.05)

# Select relevant columns
data = data[['sentiment','tweet']]

# Replace "0" with negative and "4" with positive
replace = {0 : "negative",
           4 : "postive"}
data.sentiment.replace(replace, inplace = True)

# Find all user mentions in tweets using @ and then remove them
data.tweet = data.tweet.apply(lambda text : re.sub(r'\@\w+', '',text))

# Remove all urls from tweets
url_regex = '(?i)http[s]?[://](?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
data.tweet = data.tweet.apply(lambda text : re.sub(url_regex, '',text))


# Split the data into 70% train and 30% test
train,test = train_test_split(data,test_size = 0.3)

# Save train and test dataset in data folder
train.to_csv('data/train.csv',index = False)
test.to_csv('data/test.csv',index = False)