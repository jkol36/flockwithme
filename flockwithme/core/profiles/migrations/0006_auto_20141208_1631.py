# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_remove_socialprofile_first_query'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialprofile',
            name='first_query',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='last_follower',
            field=models.IntegerField(default=None, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='last_friend',
            field=models.IntegerField(default=None, null=True),
            preserve_default=True,
        ),
    ]
