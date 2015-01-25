# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0003_twitterlist_is_queried'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='status',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[(b'complete', b'complete'), (b'interrupted', b'interrupted'), (b'paused', b'paused'), (b'started', b'started')]),
            preserve_default=True,
        ),
    ]
