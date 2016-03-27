# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20160319_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='last_login',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
