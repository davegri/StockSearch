# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawlers', '0009_auto_20150930_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crawler',
            name='origin',
            field=models.CharField(choices=[('PX', 'Pexels'), ('MG', 'Magdeleine'), ('FC', 'FancyCrave'), ('SS', 'StockSnap')], max_length=2),
        ),
        migrations.AlterField(
            model_name='image',
            name='origin',
            field=models.CharField(choices=[('PX', 'Pexels'), ('MG', 'Magdeleine'), ('FC', 'FancyCrave'), ('SS', 'StockSnap')], max_length=2),
        ),
    ]
