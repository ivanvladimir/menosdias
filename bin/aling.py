#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import print_function

import argparse
import datetime
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

    for post in posts:
        date=post['date']
        print(date)
        try:
            tweets[date]
        except KeyError:
            pass

       
