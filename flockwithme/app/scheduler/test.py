from pq import Queue, Flow
from pq.decorators import Job
from datetime import datetime
from django.conf import settings


@Job('default')
def say_hello():
	return("Hello")


