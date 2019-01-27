#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 11:30:00 2019

@author: riptide
"""

from flask import Flask

app = Flask(__name__)

from api import routes