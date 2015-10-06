# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawlers', '0004_auto_20150929_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='thumbnail',
            field=models.ImageField(upload_to='thumbs', null=True),
        ),
    ]
