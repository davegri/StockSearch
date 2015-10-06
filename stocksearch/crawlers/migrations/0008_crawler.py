# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawlers', '0007_auto_20150930_1721'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crawler',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('origin', models.CharField(max_length=2, choices=[('PX', 'pexels'), ('MG', 'magdeleine'), ('W3', 'web3')])),
                ('current_page', models.IntegerField(default=1)),
                ('images_scraped', models.IntegerField(default=0)),
            ],
        ),
    ]
