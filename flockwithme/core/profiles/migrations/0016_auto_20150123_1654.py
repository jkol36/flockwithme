# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0015_socialprofile_profile_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialprofile',
            name='profile_status',
            field=models.CharField(blank=True, max_length=150, null=True, choices=[(b'active', b'on_auto_pilot'), (b'paused', b'paused'), (b'cleaning_up', b'fixing following to follower ratio'), (b'pending', b'actions are pending.')]),
            preserve_default=True,
        ),
    ]
