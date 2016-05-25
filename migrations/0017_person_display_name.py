# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_auto_20160508_0850'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='display_name',
            field=models.CharField(max_length=30, default='temp'),
            preserve_default=False,
        ),
    ]
