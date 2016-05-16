# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20160501_1907'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='display_name',
        ),
        migrations.AddField(
            model_name='person',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='person',
            name='datecolor',
            field=models.CharField(default='#000000', max_length=20),
        ),
        migrations.AddField(
            model_name='person',
            name='email',
            field=models.CharField(max_length=40, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='meetup_name',
            field=models.CharField(max_length=40, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='notes',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='phone_a',
            field=models.CharField(max_length=15, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='phone_b',
            field=models.CharField(max_length=15, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='published_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='twitter_name',
            field=models.CharField(max_length=40, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='attendeescolor',
            field=models.CharField(default='#00C000', max_length=20),
        ),
        migrations.AlterField(
            model_name='person',
            name='backgroundcolor',
            field=models.CharField(default='#F3FFF3', max_length=20),
        ),
        migrations.AlterField(
            model_name='person',
            name='detailcolor',
            field=models.CharField(default='#0000C0', max_length=20),
        ),
    ]
