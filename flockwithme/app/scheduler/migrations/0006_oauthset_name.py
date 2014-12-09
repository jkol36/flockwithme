# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0005_auto_20141209_1735'),
    ]

    operations = [
        migrations.AddField(
            model_name='oauthset',
            name='name',
            field=models.CharField(default=b'TokenSet%d', max_length=250),
            preserve_default=True,
        ),
    ]
