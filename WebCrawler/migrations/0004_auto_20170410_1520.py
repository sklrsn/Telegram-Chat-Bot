# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-10 12:20
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebCrawler', '0003_auto_20170410_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messageholder',
            name='message_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 10, 15, 20, 49, 453802)),
        ),
    ]
