from django.contrib import admin
from .models import *

class StatusAdmin(admin.ModelAdmin):
	list_display = ('twitter_id', 'text')

class TwitterUserAdmin(admin.ModelAdmin):
	list_display = ('twitter_id', 'screen_name')

class RelationshipAdmin(admin.ModelAdmin):
	list_display = ('socialProfile', 'twitterUser', 'twitterStatus', 'created_at', 'action', 'is_initial')

class influencerAdmin(admin.ModelAdmin):
	list_display = ('created_at', 'screen_name', 'twitter_id', 'followers_count', 'favorites_count', 'tweet_count')

class TwitterListAdmin(admin.ModelAdmin):
	list_display = ('name', 'owner', 'profile')

admin.site.register(Job)
admin.site.register(Hashtag)
admin.site.register(Influencer, influencerAdmin)
admin.site.register(Location)
admin.site.register(TwitterStatus, StatusAdmin)
admin.site.register(TwitterUser)
admin.site.register(TwitterRelationship, RelationshipAdmin)
admin.site.register(TwitterList, TwitterListAdmin)

