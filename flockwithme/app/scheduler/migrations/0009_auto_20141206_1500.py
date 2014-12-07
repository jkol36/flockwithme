# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0008_twitterlist_profiles'),
    ]

    operations = [
        migrations.RenameField(
            model_name='twitterlist',
            old_name='profiles',
            new_name='followers',
        ),
    ]
