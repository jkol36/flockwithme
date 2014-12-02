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

class ListsAdmin(admin.ModelAdmin):
	list_display = ('created_at', 'name', 'profile', 'number_of_members')
class List_memberAdmin(admin.ModelAdmin):
	list_display = ('twitter_user_instance', 'list_instance')
class List_OwnerAdmin(admin.ModelAdmin):
	list_display = ('twitter_user_instance', 'list_instance')

admin.site.register(Job)
admin.site.register(Hashtag)
admin.site.register(Influencer, influencerAdmin)
admin.site.register(Location)
admin.site.register(TwitterStatus, StatusAdmin)
admin.site.register(TwitterUser)
admin.site.register(TwitterRelationship, RelationshipAdmin)
admin.site.register(Lists, ListsAdmin)
admin.site.register(List_member, List_memberAdmin)
admin.site.register(List_owner, List_OwnerAdmin)
