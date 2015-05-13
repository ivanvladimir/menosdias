#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import print_function

import re
import json

date_tweet_re=re.compile('(?P<date>\d*/\d*/\d*) (?P<tweet>.*$)')


class Tweets:
    def __init__(self,filename):
        self.tweets=[]
        self.index=0
        for line in open(filename):
            line=line.strip()
            if line.startswith('--'):
                self.tweets.append((date,texto))
            m=date_tweet_re.match(line)
            if m:
                date=m.group('date')
                texto=m.group('tweet')
        if len(date)>0:
            self.tweets.append((date,texto))

    def __iter__(self):
        return self

    def next(self):
         try:
            self.index += 1
            return self.tweets[self.index]
         except IndexError:
             raise StopIteration

class Posts:
    def __init__(self,filename):
        self.posts=[]
        self.index=0
        with open(filename) as data_file:    
            self.posts = json.load(data_file)

    def __iter__(self):
        return self

    def next(self):
         try:
            self.index += 1
            return self.tweets[self.index]
         except IndexError:
             raise StopIteration
