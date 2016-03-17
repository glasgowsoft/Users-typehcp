# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20160311_1903'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Userprofile',
            new_name='Person',
        ),
    ]
