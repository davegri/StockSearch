# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawlers', '0020_image_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='hash',
            field=models.CharField(max_length=200),
        ),
    ]
