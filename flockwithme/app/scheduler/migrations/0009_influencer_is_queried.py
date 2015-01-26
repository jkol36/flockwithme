# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0008_twitterstatus_favorited_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='influencer',
            name='is_queried',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
