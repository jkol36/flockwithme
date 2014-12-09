# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0003_oauthset'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='oauthset',
            name='name',
        ),
    ]
