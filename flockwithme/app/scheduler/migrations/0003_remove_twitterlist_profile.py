# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0002_twitterlist_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='twitterlist',
            name='profile',
        ),
    ]
