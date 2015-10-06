# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawlers', '0019_auto_20151003_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='hash',
            field=models.CharField(max_length=20, default=''),
            preserve_default=False,
        ),
    ]
