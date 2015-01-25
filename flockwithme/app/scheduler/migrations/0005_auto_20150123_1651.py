# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0004_job_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='action',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[(b'FOLLOW', b'Follow'), (b'FAVORITE', b'Favorite tweets'), (b'UNFOLLOW', b"Unfollow all the users that haven't followed you back"), (b'AUTO_DM', b'Send direct messages to your followers'), (b'TRACK_FOLLOWERS', b'Track followers'), (b'GET_ACCOUNT_INFO', b'get_account_info')]),
            preserve_default=True,
        ),
    ]
