# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0008_auto_20141227_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitterlistowner',
            name='is_queried',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='twitterlistowner',
            name='owns_lists',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
