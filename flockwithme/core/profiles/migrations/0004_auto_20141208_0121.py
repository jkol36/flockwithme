# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_socialprofile_first_query'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialprofile',
            name='first_query',
            field=models.BooleanField(default=True),
        ),
    ]
