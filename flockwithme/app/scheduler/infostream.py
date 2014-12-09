#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from Threader import Thread
import sys
from optParse import OptionParser
import tweepy
import time

class infostreamer(Thread):
	def __init__(self, lock=None, *args, **kwargs):
