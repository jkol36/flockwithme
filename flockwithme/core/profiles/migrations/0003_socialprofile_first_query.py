# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_remove_socialprofile_first_query'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialprofile',
            name='first_query',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
