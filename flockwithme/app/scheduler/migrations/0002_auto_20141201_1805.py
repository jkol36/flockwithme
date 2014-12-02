# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scheduler', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='List_member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='List_owner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Lists',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, unique=True, null=True, blank=True)),
                ('number_of_members', models.PositiveIntegerField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('profile', models.ForeignKey(related_name=b'lists', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='list',
            name='profiles',
        ),
        migrations.DeleteModel(
            name='List',
        ),
        migrations.AddField(
            model_name='list_owner',
            name='list_instance',
            field=models.ForeignKey(to='scheduler.Lists'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='list_owner',
            name='twitter_user_instance',
            field=models.ForeignKey(to='scheduler.TwitterUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='list_member',
            name='list_instance',
            field=models.ForeignKey(to='scheduler.Lists'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='list_member',
            name='twitter_user_instance',
            field=models.ForeignKey(to='scheduler.TwitterUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='job',
            name='lists',
            field=models.ForeignKey(related_name=b'follow_members_of_list', blank=True, to='scheduler.Lists', null=True),
            preserve_default=True,
        ),
    ]
