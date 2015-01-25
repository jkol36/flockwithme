# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0018_auto_20150124_0112'),
        ('scheduler', '0007_twitterrelationship_influencer'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitterstatus',
            name='favorited_by',
            field=models.ForeignKey(related_name='Favorite_Statuses', blank=True, to='profiles.SocialProfile', null=True),
            preserve_default=True,
        ),
    ]
