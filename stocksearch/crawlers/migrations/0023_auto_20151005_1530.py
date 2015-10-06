# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawlers', '0022_auto_20151004_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crawler',
            name='origin',
            field=models.CharField(choices=[('PX', 'Pexels'), ('MG', 'Magdeleine'), ('FC', 'FancyCrave'), ('SS', 'StockSnap'), ('PB', 'PixaBay'), ('TP', 'tookapic'), ('KP', 'kaboompics'), ('PJ', 'picjumbo'), ('LS', 'LibreShot'), ('LV', 'Littlevisuals'), ('SP', 'SKITTERPHOTO')], max_length=2),
        ),
        migrations.AlterField(
            model_name='image',
            name='origin',
            field=models.CharField(choices=[('PX', 'Pexels'), ('MG', 'Magdeleine'), ('FC', 'FancyCrave'), ('SS', 'StockSnap'), ('PB', 'PixaBay'), ('TP', 'tookapic'), ('KP', 'kaboompics'), ('PJ', 'picjumbo'), ('LS', 'LibreShot'), ('LV', 'Littlevisuals'), ('SP', 'SKITTERPHOTO')], max_length=2),
        ),
    ]
