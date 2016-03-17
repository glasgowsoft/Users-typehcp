# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_profile_first_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Userprofile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=20, default='a')),
                ('first_name', models.CharField(max_length=30, default='a')),
                ('email', models.EmailField(max_length=254, default='a@gmail.com')),
                ('password', models.CharField(max_length=30, default='a')),
                ('authorname', models.CharField(max_length=20, default='a')),
                ('status', models.IntegerField(default=0)),
                ('date_joined', models.DateField(default=django.utils.timezone.now)),
                ('landline', models.CharField(null=True, max_length=13, blank=True)),
                ('mobile', models.CharField(null=True, max_length=13, blank=True)),
                ('postal_address', models.CharField(null=True, max_length=200, blank=True)),
                ('notes', models.TextField(null=True, blank=True)),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
