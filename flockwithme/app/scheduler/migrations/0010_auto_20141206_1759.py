# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0009_auto_20141206_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitteruser',
            name='has_lists',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='job',
            name='action',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[(b'FOLLOW_HASHTAG', b'Follow users based on hashtags'), (b'FOLLOW_BACK', b'Follow back your followers'), (b'FAVORITE', b'Favorite tweets'), (b'UNFOLLOW_BACK', b"Unfollow all the users that haven't followed you back"), (b'UNFOLLOW_ALL', b'Unfollow everyone you currently follow'), (b'AUTO_DM', b'Send direct messages to your followers'), (b'FOLLOW_INFLUENCER', b'Follow people who follow certain accounts.'), (b'FOLLOW_MEMBERS_OF_LIST', b'Follow the members of a specific list'), (b'TRACK_FOLLOWERS', b'Track followers'), (b'GET_FOLLOWERS', b'get_followers'), (b'GET_LISTS', b'get_lists'), (b'GET_LIST_SUBSCRIBERS', b'get_list_subscribers')]),
        ),
    ]
