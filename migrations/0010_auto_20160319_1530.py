# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20160319_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='authorname',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='person',
            name='display_name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='person',
            name='last_login',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='person',
            name='password',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='person',
            name='status',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='person',
            name='username',
            field=models.CharField(max_length=20),
        ),
    ]
