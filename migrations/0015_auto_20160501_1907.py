# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_person_detailcolor'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='attendeescolor',
            field=models.CharField(max_length=7, default='#00c000'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='backgroundcolor',
            field=models.CharField(max_length=7, default='#00c000'),
            preserve_default=False,
        ),
    ]
