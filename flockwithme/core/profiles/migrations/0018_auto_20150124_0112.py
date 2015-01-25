# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0017_socialprofile_followers_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='socialprofile',
            name='follower_count',
        ),
        migrations.RemoveField(
            model_name='socialprofile',
            name='last_follower',
        ),
        migrations.RemoveField(
            model_name='socialprofile',
            name='new_followers',
        ),
    ]
