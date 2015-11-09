# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawlers', '0017_auto_20151109_1056'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crawler',
            name='visited_urls',
        ),
        migrations.DeleteModel(
            name='Url',
        ),
    ]
