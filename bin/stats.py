#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import print_function

import argparse
from menosdias import utils
from collections import Counter

verbose = lambda *a: None 

if __name__ == "__main__":
    #Las opciones de línea de comando
    p = argparse.ArgumentParser('stats.py')
    p.add_argument("TWEETS",default=None,
            action="store", help="File with tweets")
    p.add_argument("POSTS",default=None,
            action="store", help="File with posts")
    p.add_argument("-v", "--verbose",
                action="store_true", dest="verbose",
                help="Verbose mode [Off]")
    opts = p.parse_args()

    if opts.verbose:
        def verbose(*args):
            print(*args)

    tweets=utils.Tweets(opts.TWEETS)
    posts=utils.Posts(opts.POSTS)

    cw=Counter()
    bi=Counter()
    ws,ls,ts=0,0,0
    for date,tweet in tweets:
        tweet=tweet.lower()
        ls+=len(tweet)
        tweet=tweet.split()
        ws+=len(tweet)
        cw.update(tweet)
        bi.update(zip(tweet,tweet[1:]))
        ts+=1

    print("Number of tweets        :",ts)
    print("Number of words/tweet   :",ws*1.0/ts)
    print("Number of letters/tweet :",ls*1.0/ts)
    for w,c in cw.most_common(10):
        print("{0:<20}: {1}".format(w,c))
    print("10 most common bigram :")
    for w,c in bi.most_common(10):
        print("{0:<20}: {1}".format(w,c))
      
    cw=Counter()
    bi=Counter()
    ws,ls,ts=0,0,0
    for post in posts:
        post=post['body']
        for parr in post:
            parr=parr.lower()
            ls+=len(parr)
            parr=parr.split()
            ws+=len(parr)
            cw.update(parr)
            bi.update(zip(parr,parr[1:]))
            ts+=1

    print("Number of posts        :",ts)
    print("Number of words/post   :",ws*1.0/ts)
    print("Number of letters/post :",ls*1.0/ts)
    print("10 most common words :")
    for w,c in cw.most_common(10):
        print("{0:<20}: {1}".format(w,c))
    print("10 most common bigram :")
    for w,c in bi.most_common(10):
        print("{0:<20}: {1}".format(w,c))
   
