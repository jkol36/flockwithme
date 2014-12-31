# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0012_remove_socialprofile_last_query'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialprofile',
            name='last_query',
            field=models.DateTimeField(default=None, auto_now=True, null=True),
            preserve_default=True,
        ),
    ]
