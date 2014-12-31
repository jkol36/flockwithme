# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0010_socialprofile_last_query'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialprofile',
            name='last_query',
            field=models.DateTimeField(default=None, auto_now=True, null=True),
        ),
    ]
