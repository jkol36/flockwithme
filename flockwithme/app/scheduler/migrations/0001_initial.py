# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, unique=True, null=True, blank=True)),
                ('profiles', models.ManyToManyField(related_name=b'hashtags', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Influencer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('twitter_id', models.BigIntegerField(null=True, blank=True)),
                ('screen_name', models.CharField(max_length=250)),
                ('followers_count', models.PositiveIntegerField(null=True, blank=True)),
                ('favorites_count', models.PositiveIntegerField(null=True, blank=True)),
                ('tweet_count', models.PositiveIntegerField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('profiles', models.ManyToManyField(related_name=b'influencers', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action', models.CharField(blank=True, max_length=20, null=True, choices=[(b'FOLLOW_HASHTAG', b'Follow users based on hashtags'), (b'FOLLOW_BACK', b'Follow back your followers'), (b'FAVORITE', b'Favorite tweets'), (b'UNFOLLOW_BACK', b"Unfollow all the users that haven't followed you back"), (b'UNFOLLOW_ALL', b'Unfollow everyone you currently follow'), (b'AUTO_DM', b'Send direct messages to your followers'), (b'FOLLOW_INFLUENCER', b'Follow people who follow certain accounts.'), (b'FOLLOW_MEMBERS_OF_LIST', b'Follow the members of a specific list'), (b'TRACK_FOLLOWERS', b'Track followers')])),
                ('message', models.CharField(max_length=160, null=True, blank=True)),
                ('radius', models.PositiveIntegerField(null=True, blank=True)),
                ('number', models.PositiveIntegerField(null=True, blank=True)),
                ('hashtag', models.ForeignKey(related_name=b'hashtags', blank=True, to='scheduler.Hashtag', null=True)),
                ('influencer', models.ForeignKey(related_name=b'influencers', blank=True, to='scheduler.Influencer', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, unique=True, null=True, blank=True)),
                ('members', models.PositiveIntegerField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('profiles', models.ManyToManyField(related_name=b'lists', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, null=True, blank=True)),
                ('latitude', models.FloatField(null=True, blank=True)),
                ('longitude', models.FloatField(null=True, blank=True)),
                ('profiles', models.ManyToManyField(related_name=b'locations', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TwitterRelationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action', models.CharField(max_length=20, choices=[(b'FOLLOWER', b'Follower'), (b'FRIEND', b'Friend'), (b'UNFRIEND', b'Unfriended'), (b'FAVORITE', b'Favorite'), (b'DM', b'Direct Message')])),
                ('message', models.CharField(max_length=160, null=True, blank=True)),
                ('is_initial', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('socialProfile', models.ForeignKey(related_name=b'relationships', to='profiles.SocialProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TwitterStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('twitter_id', models.BigIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('text', models.CharField(max_length=160)),
                ('favorite_count', models.PositiveIntegerField(null=True, blank=True)),
                ('retweet_count', models.PositiveIntegerField(null=True, blank=True)),
                ('hashtags', models.ManyToManyField(related_name=b'statuses', null=True, to='scheduler.Hashtag', blank=True)),
                ('relationships', models.ManyToManyField(to='profiles.SocialProfile', through='scheduler.TwitterRelationship')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TwitterUser',
            fields=[
                ('screen_name', models.CharField(max_length=40, null=True, blank=True)),
                ('twitter_id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('verified', models.BooleanField(default=False)),
                ('followers_count', models.PositiveIntegerField(null=True, blank=True)),
                ('favorites_count', models.PositiveIntegerField(null=True, blank=True)),
                ('friends_count', models.PositiveIntegerField(null=True, blank=True)),
                ('location', models.CharField(max_length=100, null=True, blank=True)),
                ('statuses_count', models.PositiveIntegerField(null=True, blank=True)),
                ('relationships', models.ManyToManyField(to='profiles.SocialProfile', through='scheduler.TwitterRelationship')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='twitterstatus',
            name='twitter_user',
            field=models.ForeignKey(blank=True, to='scheduler.TwitterUser', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='twitterrelationship',
            name='twitterStatus',
            field=models.ForeignKey(blank=True, to='scheduler.TwitterStatus', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='twitterrelationship',
            name='twitterUser',
            field=models.ForeignKey(blank=True, to='scheduler.TwitterUser', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='job',
            name='location',
            field=models.ForeignKey(related_name=b'locations', blank=True, to='scheduler.Location', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='job',
            name='socialprofile',
            field=models.ForeignKey(related_name=b'jobs', to='profiles.SocialProfile'),
            preserve_default=True,
        ),
    ]
