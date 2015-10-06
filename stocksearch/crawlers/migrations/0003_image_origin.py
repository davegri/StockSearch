# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawlers', '0002_auto_20150929_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='origin',
            field=models.TextField(choices=[('pexels', 'pexels'), ('web2', 'web2'), ('web3', 'web3')], default=('pexels', 'pexels')),
            preserve_default=False,
        ),
    ]
