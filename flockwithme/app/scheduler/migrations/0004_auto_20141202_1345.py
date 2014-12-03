# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scheduler', '0003_list_owner_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='TwitterList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, unique=True, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(related_name=b'Twitter_List_Owner', default=None, to='scheduler.TwitterUser')),
                ('profile', models.ForeignKey(related_name=b'profile_lists', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('subscribers', models.ManyToManyField(default=None, related_name=b'List_Subscribers', to='scheduler.TwitterUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='list_member',
            name='list_instance',
        ),
        migrations.RemoveField(
            model_name='list_member',
            name='twitter_user_instance',
        ),
        migrations.DeleteModel(
            name='List_member',
        ),
        migrations.RemoveField(
            model_name='list_owner',
            name='list_instance',
        ),
        migrations.RemoveField(
            model_name='list_owner',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='list_owner',
            name='twitter_user_instance',
        ),
        migrations.DeleteModel(
            name='List_owner',
        ),
        migrations.RemoveField(
            model_name='lists',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='job',
            name='lists',
        ),
        migrations.DeleteModel(
            name='Lists',
        ),
        migrations.AlterField(
            model_name='job',
            name='action',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[(b'FOLLOW_HASHTAG', b'Follow users based on hashtags'), (b'FOLLOW_BACK', b'Follow back your followers'), (b'FAVORITE', b'Favorite tweets'), (b'UNFOLLOW_BACK', b"Unfollow all the users that haven't followed you back"), (b'UNFOLLOW_ALL', b'Unfollow everyone you currently follow'), (b'AUTO_DM', b'Send direct messages to your followers'), (b'FOLLOW_INFLUENCER', b'Follow people who follow certain accounts.'), (b'FOLLOW_MEMBERS_OF_LIST', b'Follow the members of a specific list'), (b'TRACK_FOLLOWERS', b'Track followers'), (b'GET_FOLLOWERS', b'get_followers')]),
        ),
    ]
