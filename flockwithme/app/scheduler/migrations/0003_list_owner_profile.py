# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scheduler', '0002_auto_20141201_1805'),
    ]

    operations = [
        migrations.AddField(
            model_name='list_owner',
            name='profile',
            field=models.ForeignKey(related_name=b'list_owner_profiles', default=None, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
