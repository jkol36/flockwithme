# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0010_auto_20141206_1759'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='twitter_list',
        ),
        migrations.AddField(
            model_name='job',
            name='owner',
            field=models.CharField(max_length=250, null=True, blank=True),
            preserve_default=True,
        ),
    ]
