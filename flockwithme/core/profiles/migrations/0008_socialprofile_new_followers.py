# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_socialprofile_num_followers'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialprofile',
            name='new_followers',
            field=models.IntegerField(default=None, null=True),
            preserve_default=True,
        ),
    ]
