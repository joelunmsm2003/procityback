# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-01-17 03:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0039_auto_20180101_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategoria',
            name='photo',
            field=models.FileField(blank=True, null=True, upload_to='static'),
        ),
    ]