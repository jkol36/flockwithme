# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0004_auto_20141227_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twitterlist',
            name='owner',
            field=models.ForeignKey(related_name=b'Owner_Of_List', default=None, to='scheduler.TwitterListOwner'),
        ),
    ]
