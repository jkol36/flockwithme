FIBCACHE = {0: 1, 1: 1}

def fib(n):
	if n in FIBCACHE:
		return FIBCACHE[n]
	else:
		FIBCACHE[n] = fib(n-1) + fib(n-2)
		return FIBCACHE[n]

print fib(24)