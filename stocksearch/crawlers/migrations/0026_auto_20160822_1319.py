# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawlers', '0025_auto_20160822_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crawler',
            name='origin',
            field=models.CharField(max_length=2, choices=[('PX', 'Pexels'), ('MG', 'Magdeleine'), ('FC', 'FancyCrave'), ('SS', 'StockSnap'), ('PB', 'PixaBay'), ('TP', 'tookapic'), ('KP', 'kaboompics'), ('PJ', 'picjumbo'), ('LS', 'LibreShot'), ('LV', 'Littlevisuals'), ('SP', 'SKITTERPHOTO'), ('JM', 'JayMantri'), ('MT', 'MMT'), ('FN', 'FreeNatureStock'), ('BA', 'BARA ART'), ('FP', 'Freely Photos'), ('BI', 'Barn Images'), ('GS', 'GoodStockPhotos'), ('IP', 'Finda Photo'), ('PG', 'Picography'), ('NS', 'Negative Space'), ('SH', 'SplitShire'), ('RS', 'Realistic Shots'), ('SW', 'StreetWill'), ('BF', 'Boss Fight'), ('LP', 'LIFE OF PIX'), ('PD', 'public domain archive'), ('BL', 'Bucketlistly Photos'), ('FB', 'Free Image Bank'), ('CV', 'CREATIVE VIX'), ('DP', 'DesignerPics'), ('FS', 'freestocks'), ('TC', 'travel coffee book'), ('FF', 'FOODIES FEED'), ('MS', 'My Stock Photos'), ('IR', 'ISO Republic'), ('JS', 'jeshoots'), ('SK', 'Stokpic'), ('JH', 'Joshua Hibbert'), ('MI', 'minimography'), ('IJ', 'Pickle Jar'), ('AI', 'alana.io'), ('PA', 'picalls'), ('SF', 'Stockified'), ('LG', 'LOOKING GLASS'), ('NP', 'nomad_pictures'), ('AP', 'AVOPIX')]),
        ),
        migrations.AlterField(
            model_name='image',
            name='origin',
            field=models.CharField(max_length=2, choices=[('PX', 'Pexels'), ('MG', 'Magdeleine'), ('FC', 'FancyCrave'), ('SS', 'StockSnap'), ('PB', 'PixaBay'), ('TP', 'tookapic'), ('KP', 'kaboompics'), ('PJ', 'picjumbo'), ('LS', 'LibreShot'), ('LV', 'Littlevisuals'), ('SP', 'SKITTERPHOTO'), ('JM', 'JayMantri'), ('MT', 'MMT'), ('FN', 'FreeNatureStock'), ('BA', 'BARA ART'), ('FP', 'Freely Photos'), ('BI', 'Barn Images'), ('GS', 'GoodStockPhotos'), ('IP', 'Finda Photo'), ('PG', 'Picography'), ('NS', 'Negative Space'), ('SH', 'SplitShire'), ('RS', 'Realistic Shots'), ('SW', 'StreetWill'), ('BF', 'Boss Fight'), ('LP', 'LIFE OF PIX'), ('PD', 'public domain archive'), ('BL', 'Bucketlistly Photos'), ('FB', 'Free Image Bank'), ('CV', 'CREATIVE VIX'), ('DP', 'DesignerPics'), ('FS', 'freestocks'), ('TC', 'travel coffee book'), ('FF', 'FOODIES FEED'), ('MS', 'My Stock Photos'), ('IR', 'ISO Republic'), ('JS', 'jeshoots'), ('SK', 'Stokpic'), ('JH', 'Joshua Hibbert'), ('MI', 'minimography'), ('IJ', 'Pickle Jar'), ('AI', 'alana.io'), ('PA', 'picalls'), ('SF', 'Stockified'), ('LG', 'LOOKING GLASS'), ('NP', 'nomad_pictures'), ('AP', 'AVOPIX')]),
        ),
    ]
