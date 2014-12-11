# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0003_oauthset_rate_limited'),
    ]

    operations = [
        migrations.AddField(
            model_name='oauthset',
            name='last_used',
            field=models.DateTimeField(auto_now=True, null=True),
            preserve_default=True,
        ),
    ]
