# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_auto_20141230_2026'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialprofile',
            name='last_query',
            field=models.DateTimeField(default=None, auto_now=True),
            preserve_default=True,
        ),
    ]
