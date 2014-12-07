# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0006_auto_20141205_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitterlist',
            name='twitter_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
