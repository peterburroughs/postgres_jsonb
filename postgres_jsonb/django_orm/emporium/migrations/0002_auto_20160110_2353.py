# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-11 04:53
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emporium', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bargain',
            name='info',
            field=django.contrib.postgres.fields.jsonb.JSONField(db_index=True),
        ),
    ]
