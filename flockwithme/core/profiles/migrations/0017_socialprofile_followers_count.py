# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0016_auto_20150123_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialprofile',
            name='followers_count',
            field=models.IntegerField(default=None, null=True),
            preserve_default=True,
        ),
    ]
