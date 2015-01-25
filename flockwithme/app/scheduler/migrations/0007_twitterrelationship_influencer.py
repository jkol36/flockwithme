# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0006_influencer_friends_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitterrelationship',
            name='influencer',
            field=models.ForeignKey(related_name='relationships', blank=True, to='scheduler.Influencer', null=True),
            preserve_default=True,
        ),
    ]
