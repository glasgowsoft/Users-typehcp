# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20160316_2053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='person',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='person',
            name='email',
        ),
        migrations.RemoveField(
            model_name='person',
            name='landline',
        ),
        migrations.RemoveField(
            model_name='person',
            name='mobile',
        ),
        migrations.RemoveField(
            model_name='person',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='person',
            name='postal_address',
        ),
    ]
