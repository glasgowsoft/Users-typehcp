# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20160330_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='detailcolor',
            field=models.CharField(max_length=7, default='#0000c0'),
            preserve_default=False,
        ),
    ]
