# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0019_twitteruser_is_queried'),
    ]

    operations = [
        migrations.CreateModel(
            name='list_owner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('screen_name', models.CharField(max_length=250)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
