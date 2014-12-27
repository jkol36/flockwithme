# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0003_remove_twitterlist_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twitterlist',
            name='followers',
            field=models.ManyToManyField(related_name=b'user_instances_who_follow_this_list', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='twitterlist',
            name='owner',
            field=models.ForeignKey(related_name=b'Owner_Of_List', default=None, to='scheduler.TwitterUser'),
        ),
    ]
