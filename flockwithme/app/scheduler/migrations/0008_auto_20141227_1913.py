# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0007_twitterlistowner_followers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twitterlistowner',
            name='followers',
            field=models.ManyToManyField(related_name=b'owners', null=True, to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
