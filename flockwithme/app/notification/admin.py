from django.contrib import admin
from .models import Notification

class NotificationAdmin(admin.ModelAdmin):
	list_display = ('receiver', 'short_message', 'seen', 'created_at')

admin.site.register(Notification, NotificationAdmin)
