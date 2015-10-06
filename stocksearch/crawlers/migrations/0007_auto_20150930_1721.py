# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawlers', '0006_auto_20150930_1352'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='url',
            new_name='source_url',
        ),
        migrations.AddField(
            model_name='image',
            name='image_page_url',
            field=models.URLField(default='www.example.com'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='image',
            name='origin',
            field=models.CharField(max_length=2, choices=[('PX', 'pexels'), ('MG', 'magdeleine'), ('W3', 'web3')]),
        ),
    ]
