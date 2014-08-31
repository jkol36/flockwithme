from django import template
from itertools import izip_longest

register = template.Library()

@register.inclusion_tag('list_accounts.jade', takes_context = True)
def list_accounts(context):
	# def grouper(n, iterable, fillvalue=''):
	# 	args = [iter(iterable)] * n
	# 	return izip_longest(fillvalue=fillvalue, *args)
	# user = context['user']
	# accounts = user.accounts.all()
	# altered_list = []
	# for a, b, c in grouper(3, accounts):
	# 	altered_list.append((a,b,c))
	# return {'accounts': altered_list}
	return {'accounts': context['user'].accounts.all()}