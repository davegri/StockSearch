# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawlers', '0003_image_origin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='origin',
            field=models.CharField(max_length=2, choices=[('PX', 'pexels'), ('W2', 'web2'), ('W3', 'web3')]),
        ),
    ]
