# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0016_remove_twitteruser_querie'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitteruser',
            name='query',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
