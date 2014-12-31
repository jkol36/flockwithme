# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_socialprofile_new_followers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='socialprofile',
            old_name='last_friend',
            new_name='follower_count',
        ),
        migrations.RenameField(
            model_name='socialprofile',
            old_name='num_followers',
            new_name='friend_count',
        ),
    ]
