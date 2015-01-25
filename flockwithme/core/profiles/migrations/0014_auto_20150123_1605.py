# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0013_socialprofile_last_query'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='socialprofile',
            name='first_query',
        ),
        migrations.RemoveField(
            model_name='socialprofile',
            name='last_query',
        ),
    ]
