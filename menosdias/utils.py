#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import print_function

import re
import json
import datetime

date_re=re.compile(r'.*</menosdias> (?P<date>\d[^<]*)$')
tweetdate_re=re.compile(r'de (?P<mes>\w+\.) de')

def tweetdate2date(date):
    m=tweetdate_re.search(date)
    if m:
        if m.group('mes'):
            date=date.replace(' de ene. de ','/01/')
            date=date.replace(' de feb. de ','/02/')
            date=date.replace(' de mar. de ','/03/')
            date=date.replace(' de abr. de ','/04/')
            date=date.replace(' de may. de ','/05/')
            date=date.replace(' de jun. de ','/06/')
            date=date.replace(' de jul. de ','/07/')
            date=date.replace(' de ago. de ','/08/')
            date=date.replace(' de sept. de ','/08/')
            date=date.replace(' de oct. de ','/10/')
            date=date.replace(' de nov. de ','/11/')
            date=date.replace(' de dic. de ','/12/')
    return datetime.datetime.strptime(date,"%d/%m/%Y")
            


class Tweets:
    def __init__(self,filename,year='2015'):
        self.tweets=[]
        self.index=0
        self.date_={}
        c=0
        for line in open(filename):
            line=line.strip()
            if line.startswith('--'):
                if date:
                    self.tweets.append((date,texto))
                date,texto=None,None
            m=date_re.match(line)
            if m:
                date=m.group('date')
                if not date[-1].isdigit():
                    date+=" de {0}".format(year)
                date=tweetdate2date(date)
                c=0
            if c==3:
                texto=line
            c+=1
        if date:
            self.tweets.append((date,texto))
        self.date_=dict(self.tweets)

    def __iter__(self):
        return self

    def __getitem__(self,index):
        return self.date_[index]

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
        for post in self.posts:
            post['date']=datetime.datetime.strptime(post['datePublished'][0][:-6],"%Y-%m-%dT%H:%M:%S")

    def __iter__(self):
        return self

    def next(self):
         try:
            self.index += 1
            return self.posts[self.index]
         except IndexError:
             raise StopIteration
