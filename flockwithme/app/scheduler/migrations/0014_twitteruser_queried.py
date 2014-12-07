# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0013_twitteruser_has_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitteruser',
            name='queried',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
