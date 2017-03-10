# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-10 05:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finder', '0003_auto_20170309_2010'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='autoUpdate',
            field=models.BooleanField(db_column='Will Update via Query?', default=True),
        ),
        migrations.AddField(
            model_name='embassy',
            name='autoUpdate',
            field=models.BooleanField(db_column='Will Update via Query?', default=True),
        ),
    ]
