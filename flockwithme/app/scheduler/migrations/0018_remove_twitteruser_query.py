# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0017_twitteruser_query'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='twitteruser',
            name='query',
        ),
    ]
