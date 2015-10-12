# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawlers', '0024_auto_20151006_0351'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='crawler',
            name='origin',
            field=models.CharField(max_length=2, choices=[('PX', 'Pexels'), ('MG', 'Magdeleine'), ('FC', 'FancyCrave'), ('SS', 'StockSnap'), ('PB', 'PixaBay'), ('TP', 'tookapic'), ('KP', 'kaboompics'), ('PJ', 'picjumbo'), ('LS', 'LibreShot'), ('LV', 'Littlevisuals'), ('SP', 'SKITTERPHOTO'), ('JM', 'JayMantri'), ('MT', 'MMT')]),
        ),
        migrations.AlterField(
            model_name='image',
            name='hash',
            field=models.CharField(max_length=576),
        ),
        migrations.AlterField(
            model_name='image',
            name='origin',
            field=models.CharField(max_length=2, choices=[('PX', 'Pexels'), ('MG', 'Magdeleine'), ('FC', 'FancyCrave'), ('SS', 'StockSnap'), ('PB', 'PixaBay'), ('TP', 'tookapic'), ('KP', 'kaboompics'), ('PJ', 'picjumbo'), ('LS', 'LibreShot'), ('LV', 'Littlevisuals'), ('SP', 'SKITTERPHOTO'), ('JM', 'JayMantri'), ('MT', 'MMT')]),
        ),
    ]
