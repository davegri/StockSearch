# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawlers', '0011_auto_20151001_0211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crawler',
            name='origin',
            field=models.CharField(choices=[('PX', 'Pexels'), ('MG', 'Magdeleine'), ('FC', 'FancyCrave'), ('SS', 'StockSnap'), ('PB', 'PixaBay'), ('TP', 'tookapic')], max_length=2),
        ),
        migrations.AlterField(
            model_name='image',
            name='image_page_url',
            field=models.URLField(unique=True, max_length=400),
        ),
        migrations.AlterField(
            model_name='image',
            name='origin',
            field=models.CharField(choices=[('PX', 'Pexels'), ('MG', 'Magdeleine'), ('FC', 'FancyCrave'), ('SS', 'StockSnap'), ('PB', 'PixaBay'), ('TP', 'tookapic')], max_length=2),
        ),
        migrations.AlterField(
            model_name='image',
            name='source_url',
            field=models.URLField(max_length=400),
        ),
    ]
