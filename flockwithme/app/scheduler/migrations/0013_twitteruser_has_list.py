# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0012_remove_twitteruser_has_lists'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitteruser',
            name='has_list',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
