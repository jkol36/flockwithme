# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0018_auto_20150124_0112'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialprofile',
            name='twitter_id',
            field=models.IntegerField(default=None, null=True),
            preserve_default=True,
        ),
    ]
