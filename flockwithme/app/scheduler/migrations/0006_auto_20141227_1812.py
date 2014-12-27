# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0005_auto_20141227_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twitterlist',
            name='followers',
            field=models.ManyToManyField(related_name=b'List_following', to=settings.AUTH_USER_MODEL),
        ),
    ]
