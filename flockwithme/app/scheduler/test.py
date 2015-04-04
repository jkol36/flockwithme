from pq import Queue, Flow, Worker
from pq.decorators import Job
from datetime import datetime
from django.conf import settings


q = Queue()
w = Worker(q)
with Flow(q, name="my_flow") as f:
	f.enqueue(func=my_first_task)

	f.jobs

	# A Flow is stored in a django FlowStore instance. To retrieve them.
	fs = f.get(f.id)

	# or get a queryset of FlowStore instances by name
	fs_list = fs.get('myflow')

	# This is just a shortcut for accessing the FlowStore objects directly through the orm.
	from pq.flow import FlowStore
	fs = FlowStore.objects.get(pk=f.id)
	fs = FlowStore.objects.filter(name='myflow')


