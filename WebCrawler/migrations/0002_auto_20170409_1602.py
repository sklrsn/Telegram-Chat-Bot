# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-09 13:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WebCrawler', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='messageholder',
            old_name='message_id',
            new_name='message_update_id',
        ),
    ]
