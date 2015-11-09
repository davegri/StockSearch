# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawlers', '0016_auto_20151104_1539'),
    ]

    operations = [
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('url', models.URLField(max_length=400)),
            ],
        ),
        migrations.AddField(
            model_name='crawler',
            name='visited_urls',
            field=models.ManyToManyField(to='crawlers.Url'),
        ),
    ]
