#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 20:31:15 2019

@author: riptide
"""

# Necessary imports
from joblib import load
import sys
sys.path.insert(0,'/home/riptide/Code/data_science/sentiment_analysis/api')

class SentimentAnalysis():
    
    def __init__(self):
        
        # Load tokenizer
        self.tokenizer = load('models/tokenizer.joblib')
        
        # load classifier
        self.classifier = load('models/nbclassifier.joblib')
        
        
    def get_sentiment(self,data):
        
        # Tokenize data
        tokenized_data = self.tokenizer.transform(data).toarray()
                
        # Predict Sentiment
        y_pred = self.classifier.predict(tokenized_data)
        
        # Return predicted sentiment as a list
        return y_pred.tolist()
