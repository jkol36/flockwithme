# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0014_twitteruser_queried'),
    ]

    operations = [
        migrations.RenameField(
            model_name='twitteruser',
            old_name='queried',
            new_name='querie',
        ),
    ]
