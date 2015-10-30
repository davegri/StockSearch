# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('crawlers', '0013_auto_20151030_2032'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
