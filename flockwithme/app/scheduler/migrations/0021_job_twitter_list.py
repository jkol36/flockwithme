# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0020_list_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='twitter_list',
            field=models.ForeignKey(related_name=b'twitter_lists', blank=True, to='scheduler.TwitterList', null=True),
            preserve_default=True,
        ),
    ]
