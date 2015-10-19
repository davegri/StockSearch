# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawlers', '0003_auto_20151019_1422'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SearchQuery',
        ),
    ]
