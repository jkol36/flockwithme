from pq import Queue, Flow
from pq.decorators import Job
from datetime import datetime


@Job('default')
def say_hello():
	return("Hello")


