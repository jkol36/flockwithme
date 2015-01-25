# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0014_auto_20150123_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialprofile',
            name='profile_status',
            field=models.CharField(blank=True, max_length=150, null=True, choices=[(b'active', b'on_auto_pilot'), (b'paused', b'rate_limited'), (b'cleaning_up', b'fixing following to follower ratio')]),
            preserve_default=True,
        ),
    ]
