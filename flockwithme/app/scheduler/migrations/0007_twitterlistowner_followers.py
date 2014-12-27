# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scheduler', '0006_auto_20141227_1812'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitterlistowner',
            name='followers',
            field=models.ManyToManyField(related_name=b'owner_followers', null=True, to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
    ]
