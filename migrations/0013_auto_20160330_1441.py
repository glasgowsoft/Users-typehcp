# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20160327_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='fullmember',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='person',
            name='authorname',
            field=models.CharField(null=True, blank=True, max_length=20),
        ),
    ]
