#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 02:53:18 2019

@author: riptide
"""

# Necessary Imports
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import GaussianNB
from joblib import dump

# Change working directory
os.chdir('/home/riptide/Code/data_science/sentiment_analysis')

# Read train data 
train = pd.read_csv('data/train.csv')
X_train = train['tweet']
y_train = train['sentiment']


# Create tokenizer on train data with trigram
tokenizer = TfidfVectorizer(ngram_range=(1,3),stop_words="english",min_df=5)

# Fit and Transform train data
X_train = tokenizer.fit_transform(X_train).toarray()

# Remove unneccessary dataframe
del(train)

# Make and fit classifier
NBclassifier = GaussianNB()
NBclassifier.fit(X_train, y_train)

# Read test data
test = pd.read_csv('data/test.csv')
X_test = test['tweet']
y_test = test['sentiment']

# Tokenize test data
X_test = tokenizer.transform(X_test).toarray()

# Get Accuracy on train and test
print("Train Accuracy",NBclassifier.score(X_train,y_train))
print("Test Accuracy",NBclassifier.score(X_test,y_test))

# Save the tokenizer and the model for the API
dump(tokenizer,'tokenizer.joblib')
dump(NBclassifier,'nbclassifier.joblib')

