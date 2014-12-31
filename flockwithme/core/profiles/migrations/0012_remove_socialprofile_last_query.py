# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0011_auto_20141230_2149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='socialprofile',
            name='last_query',
        ),
    ]
