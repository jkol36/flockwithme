# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0002_remove_twitterlist_quiried'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitterlist',
            name='is_queried',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
