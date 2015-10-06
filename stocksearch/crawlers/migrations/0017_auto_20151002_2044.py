# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawlers', '0016_auto_20151002_0640'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='image_page_url',
            new_name='page_url',
        ),
    ]
