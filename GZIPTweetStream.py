# -*- coding: UTF-8 -*-
import gzip, json
from twokenize import tokenize
from text_utils import *

class GZIPTweetStream(object):
    def __init__(self, files, exclude_rts=False, downcase=False):
        self.files = files
        self.exclude_rts = exclude_rts
        self.downcase = downcase
    def __iter__(self):
        for fname in self.files:
            with gzip.open(fname) as f:
                for line in f:
                    tweet = json.loads(line.strip())

                    text = tweet['text']
                    if self.exclude_rts:
                        if retweet_or_share(text) or tweet['is_rt']:
                            continue
                    text = prepare_text(text)
                    if self.downcase:
                        text = text.lower()
                    yield tokenize(text)
