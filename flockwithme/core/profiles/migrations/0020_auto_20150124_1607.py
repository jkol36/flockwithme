# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0019_socialprofile_twitter_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='socialprofile',
            name='profile_status',
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_status',
            field=models.CharField(default=b'pending', max_length=250, choices=[(b'active', b'Congratulations! All your Twitter Accounts are currently running on auto-pilot! Go out and play or something.'), (b'pending', b'all actions are currently pending. If this message lasts for more than 24 hours. Please contact us.'), (b'paused', b'actions are currently paused for all your accounts.')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='job_status',
            field=models.CharField(blank=True, max_length=150, null=True, choices=[(b'Just_Cleaned', b'We just fixed up your following/follower ratio. Next up, is to follow people and favorite tweets.'), (b'Just_Followed', b'We just followed and favorited. Next up, is to direct message your followers'), (b'Dm_Skipped', b"We couldn't direct message your followers because you didn't set a message. This process was skipped today."), (b'Just_Dmed', b'We just sent your message to your most recent followers. All actions complete for today.'), (b'Follow_Limit_Reached', b"Following people failed because you're rate limited. We'll try again tomorrow."), (b'Follow_Ratio_Off', b"Following people failed because you're following to many people. Next up is to clean up your ratio!")]),
            preserve_default=True,
        ),
    ]
