# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawlers', '0009_auto_20151016_2358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crawler',
            name='origin',
            field=models.CharField(choices=[('PX', 'Pexels'), ('MG', 'Magdeleine'), ('FC', 'FancyCrave'), ('SS', 'StockSnap'), ('PB', 'PixaBay'), ('TP', 'tookapic'), ('KP', 'kaboompics'), ('PJ', 'picjumbo'), ('LS', 'LibreShot'), ('LV', 'Littlevisuals'), ('SP', 'SKITTERPHOTO'), ('JM', 'JayMantri'), ('MT', 'MMT'), ('FN', 'FreeNatureStock'), ('BA', 'BARA ART'), ('FP', 'Freely Photos'), ('BI', 'Barn Images'), ('GS', 'GoodStockPhotos'), ('IP', 'Finda Photo'), ('PG', 'Picography'), ('NS', 'Negative Space'), ('SH', 'SplitShire'), ('RS', 'Realistic Shots'), ('SW', 'StreetWill'), ('BF', 'Boss Fight'), ('LP', 'LIFE OF PIX'), ('PD', 'public domain archive'), ('BL', 'Bucketlistly Photos'), ('FB', 'Free Image Bank'), ('CV', 'CREATIVE VIX')], max_length=2),
        ),
        migrations.AlterField(
            model_name='image',
            name='origin',
            field=models.CharField(choices=[('PX', 'Pexels'), ('MG', 'Magdeleine'), ('FC', 'FancyCrave'), ('SS', 'StockSnap'), ('PB', 'PixaBay'), ('TP', 'tookapic'), ('KP', 'kaboompics'), ('PJ', 'picjumbo'), ('LS', 'LibreShot'), ('LV', 'Littlevisuals'), ('SP', 'SKITTERPHOTO'), ('JM', 'JayMantri'), ('MT', 'MMT'), ('FN', 'FreeNatureStock'), ('BA', 'BARA ART'), ('FP', 'Freely Photos'), ('BI', 'Barn Images'), ('GS', 'GoodStockPhotos'), ('IP', 'Finda Photo'), ('PG', 'Picography'), ('NS', 'Negative Space'), ('SH', 'SplitShire'), ('RS', 'Realistic Shots'), ('SW', 'StreetWill'), ('BF', 'Boss Fight'), ('LP', 'LIFE OF PIX'), ('PD', 'public domain archive'), ('BL', 'Bucketlistly Photos'), ('FB', 'Free Image Bank'), ('CV', 'CREATIVE VIX')], max_length=2),
        ),
    ]
