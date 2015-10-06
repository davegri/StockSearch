# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawlers', '0008_crawler'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image_page_url',
            field=models.URLField(unique=True),
        ),
    ]
