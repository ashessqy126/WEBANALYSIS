# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Codes',
            fields=[
                ('code', models.CharField(max_length=200, serialize=False, primary_key=True)),
                ('flag', models.CharField(max_length=5, null=True, blank=True)),
                ('degree', models.CharField(max_length=1, null=True, blank=True)),
            ],
            options={
                'db_table': 'codes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Links',
            fields=[
                ('website', models.CharField(max_length=50)),
                ('link', models.CharField(max_length=50, serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'links',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Matchresult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('degree', models.CharField(max_length=1, null=True, blank=True)),
                ('count', models.IntegerField(null=True, blank=True)),
                ('website', models.CharField(max_length=50, null=True, blank=True)),
                ('code', models.CharField(max_length=200, null=True, blank=True)),
            ],
            options={
                'db_table': 'matchresult',
                'managed': False,
            },
        ),
    ]
