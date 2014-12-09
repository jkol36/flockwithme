# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_auto_20141208_0121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='socialprofile',
            name='first_query',
        ),
    ]
