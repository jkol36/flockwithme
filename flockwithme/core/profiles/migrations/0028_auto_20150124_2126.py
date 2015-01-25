# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0027_auto_20150124_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialprofile',
            name='job_status',
            field=models.CharField(default=b'Fetch_Account_Info', max_length=150, choices=[(b'Just_Cleaned', b'We just fixed up your following/follower ratio. Next up, is to follow people and favorite tweets.'), (b'Just_Followed', b'We just followed users. Next up, is to fetch your latest favorited tweets.'), (b'Dm_Skipped', b"We couldn't direct message your followers because you didn't set a message. This process was skipped today."), (b'Just_Dmed', b'We just sent your message to your most recent followers. All actions complete for today.'), (b'Follow_Limit_Reached', b"Following people failed because you're rate limited. We'll try again tomorrow."), (b'Follow_Ratio_Off', b"Following people failed because you're following to many people. Next up is to clean up your ratio!"), (b'Fetch_Account_Info', b'Next Up is to fetch your followers and friends.'), (b'Fetching_Account_Info', b'Currently fetching your friends and followers.'), (b'Account_Info_Fetched', b'We finished Fetching your account info. Next up is to follow people and favorite tweets.'), (b'Ratio_Good', b'Just checked your Following/Follower ratio and everything is good! Next up is to follow people and favorite Tweets.'), (b'Ratio_Bad', b'Your Ratio needs cleaning.'), (b'FAVORITES_FETCHED', b'ready to favorite tweets'), (b'Just_Favorited', b'We just favorited tweets. Next Step is to auto_dm your followers.')]),
            preserve_default=True,
        ),
    ]
