# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0004_remove_oauthset_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='oauthset',
            name='access_key',
            field=models.CharField(default=False, max_length=250),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='oauthset',
            name='c_key',
            field=models.CharField(default=False, max_length=250),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='oauthset',
            name='c_secret',
            field=models.CharField(default=False, max_length=250),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='oauthset',
            name='key_secret',
            field=models.CharField(default=False, max_length=250),
            preserve_default=True,
        ),
    ]
