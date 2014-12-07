# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0015_auto_20141206_1926'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='twitteruser',
            name='querie',
        ),
    ]
