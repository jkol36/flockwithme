# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0011_auto_20141206_1856'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='twitteruser',
            name='has_lists',
        ),
    ]
