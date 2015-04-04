from pq import Queue, Flow
from datetime import datetime


q = Queue()
def my_first_task():
	print "hello_world"
with Flow(q) as f:
	f.enqueue(my_first_task)


