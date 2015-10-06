# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawlers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='thumbnail',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]
