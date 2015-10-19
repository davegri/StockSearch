# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawlers', '0002_auto_20151015_0134'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchQuery',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('text', models.CharField(max_length=400)),
                ('amount', models.IntegerField(default=1)),
            ],
        ),
        migrations.AddField(
            model_name='image',
            name='clicks',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='crawler',
            name='origin',
            field=models.CharField(max_length=2, choices=[('PX', 'Pexels'), ('MG', 'Magdeleine'), ('FC', 'FancyCrave'), ('SS', 'StockSnap'), ('PB', 'PixaBay'), ('TP', 'tookapic'), ('KP', 'kaboompics'), ('PJ', 'picjumbo'), ('LS', 'LibreShot'), ('LV', 'Littlevisuals'), ('SP', 'SKITTERPHOTO'), ('JM', 'JayMantri'), ('MT', 'MMT'), ('FN', 'FreeNatureStock'), ('BA', 'BARA ART'), ('FP', 'Freely Photos'), ('BI', 'Barn Images'), ('GS', 'GoodStockPhotos'), ('IP', 'Finda Photo'), ('PG', 'Picography'), ('NS', 'Negative Space'), ('SH', 'SplitShire'), ('RS', 'Realistic Shots'), ('SW', 'StreetWill'), ('BF', 'Boss Fight'), ('LP', 'LIFE OF PIX'), ('PD', 'public domain archive'), ('BL', 'Bucketlistly Photos'), ('FB', 'Free Image Bank'), ('CV', 'CREATIVE VIX')]),
        ),
        migrations.AlterField(
            model_name='image',
            name='origin',
            field=models.CharField(max_length=2, choices=[('PX', 'Pexels'), ('MG', 'Magdeleine'), ('FC', 'FancyCrave'), ('SS', 'StockSnap'), ('PB', 'PixaBay'), ('TP', 'tookapic'), ('KP', 'kaboompics'), ('PJ', 'picjumbo'), ('LS', 'LibreShot'), ('LV', 'Littlevisuals'), ('SP', 'SKITTERPHOTO'), ('JM', 'JayMantri'), ('MT', 'MMT'), ('FN', 'FreeNatureStock'), ('BA', 'BARA ART'), ('FP', 'Freely Photos'), ('BI', 'Barn Images'), ('GS', 'GoodStockPhotos'), ('IP', 'Finda Photo'), ('PG', 'Picography'), ('NS', 'Negative Space'), ('SH', 'SplitShire'), ('RS', 'Realistic Shots'), ('SW', 'StreetWill'), ('BF', 'Boss Fight'), ('LP', 'LIFE OF PIX'), ('PD', 'public domain archive'), ('BL', 'Bucketlistly Photos'), ('FB', 'Free Image Bank'), ('CV', 'CREATIVE VIX')]),
        ),
    ]
