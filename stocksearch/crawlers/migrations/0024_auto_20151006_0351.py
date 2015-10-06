# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawlers', '0023_auto_20151005_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='hash',
            field=models.CharField(max_length=1000),
        ),
    ]
