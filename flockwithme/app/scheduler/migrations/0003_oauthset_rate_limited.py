# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0002_oauthset_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='oauthset',
            name='rate_limited',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
