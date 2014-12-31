import os
import time
import sys
import tweepy

class subscriberFetcher(object):
	def __init__(self, twitterlists, *args, **kwargs):
		self.twitterlists = kwargs.pop('TwitterLists')
		return super(subscriberFetcher, self).__init__(*args, **kwargs)


class 