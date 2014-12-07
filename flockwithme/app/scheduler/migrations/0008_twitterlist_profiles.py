# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scheduler', '0007_twitterlist_twitter_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitterlist',
            name='profiles',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
