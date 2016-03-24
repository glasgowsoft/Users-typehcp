# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20160319_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='last_login',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
