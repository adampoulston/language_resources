# -*- coding: UTF-8 -*-
import csv
import re
import string
from emoji_codes import *
from twokenize import tokenize
from random import choice

#Regular expressions for stripping text
url_re = re.compile(r"(http|ftp|https)(:\/\/)([\w\-_]+(?:(?:\.[\w\-_]+)+))([\w\-\.,@?^=%&amp;:\/~\+#]*[\w\-\@?^=%&amp;\/~\+#])?")
mention_re = re.compile(r"(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z0-9\_]+[A-Za-z0-9\_]+)")
word_pad_re = re.compile(r"(.{2})\1{1,}")
#matches alphanumeric and # + @
alphanumeric_only_re = re.compile('([^\s\w#@]|_)+', re.UNICODE)
quotation_re = re.compile(r'(["“])((?:(?!\1)[^\\]|(?:\\\\)*\\[^\\])*)(\1)')

try:
    # Wide UCS-4 build
    emoji_re = re.compile(u'['
        u'\U0001F300-\U0001F64F'
        u'\U0001F680-\U0001F6FF'
        u'\u2600-\u26FF\u2700-\u27BF]', 
        re.UNICODE)
except re.error:
    # Narrow UCS-2 build
    emoji_re = re.compile(u'('
        u'\ud83c[\udf00-\udfff]|'
        u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
        u'[\u2600-\u26FF\u2700-\u27BF])', 
        re.UNICODE)

#matches retweets and shares through non-twitter methods
rt_re = re.compile(r'\b(rt|retweet|via)(?:\b\W*@(\w+))+')
share_re = re.compile(r'\b(via)(?:\b\W*(http|www)+)')

def retweet_or_share(t):
    #check for unofficial retweets
    rt_matches = rt_re.findall(t)
    share_matches = share_re.findall(t)

    checks = [
        len(rt_matches) == 0,
        len(share_matches) == 0
    ]

    return all(checks)

def lookup_emoji(unicode_string):
		try:
			return UNICODE_EMOJI[unicode_string]
		except:
			return "no_emoji_description"

def prepare_text(text, url_scheme='st', strip_word_padding=False, alphanumeric_only = False, strip_quotations=False):
    """
        Prepares the raw tweet text for tokenisation, then tokenizes it using twokenize (https://github.com/ianozsvald/ark-tweet-nlp-python)
    """
    try:
        #convert to unicode of needs be
        text = unicode(text, "utf8")
    except:
        pass

    #strip trailing whitespace
    text = text.strip()

    #replace silly quotes with real ones for the regex to work
    text = text.replace(u'“', u'"').replace(u'”',u'"')

    #replace newlines with a special token
    text = text.replace("\n", " ").replace("\r", "")
    text = re.sub(mention_re, "@mention", text)
    #handle URLS
    # possible schemes 'st': single token, 'leave'
    if url_scheme != 'leave':
        text = re.sub(url_re, "@hyperlink", text)

    # reduce extended words to a shorter token. e.g. "reeeeeeeeeee"->"ree", "hahahaha" -> "haha"
    if strip_word_padding:
        #TODO: make this work
        pass

    # add spaces between emoji and attach description
    for match in list(set(emoji_re.findall(text))):
        emoji_description = lookup_emoji(match)
        text = text.replace(match," "+match+"_"+emoji_description+" ")

    # strip out non AN characters (except # and @)
    if alphanumeric_only:
        text = re.sub(alphanumeric_only_re, "", text)

    if strip_quotations:
        text = re.sub(quotation_re, "@quote", text)

    return text

def extract_emoji(text):
    try:
        text = unicode(text, "utf8")
    except:
        pass
    emo_string = ""
    for match in list(set(emoji_re.findall(text))):
        emoji_description = lookup_emoji(match)
        emo_string += " "+match+"_"+emoji_description

    return emo_string

def rand_str(n=15):
    return ''.join([choice(string.ascii_lowercase) for _ in range(n)])
