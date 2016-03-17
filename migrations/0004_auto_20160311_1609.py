# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20160311_1554'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user_author',
        ),
        migrations.AddField(
            model_name='profile',
            name='authorname',
            field=models.CharField(max_length=20, default='a'),
        ),
    ]
