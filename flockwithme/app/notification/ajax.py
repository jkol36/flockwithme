from django_ajax.decorators import ajax

@ajax
def seen_view(request):
	for notification in request.user.notifications.filter(seen=False):
		notification.seen = True
		notification.save()
	return {'inner-fragments': {'#notification-badge': 0}}