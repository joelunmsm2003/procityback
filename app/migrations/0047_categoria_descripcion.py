# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-02-11 19:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0046_auto_20180128_1948'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoria',
            name='descripcion',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
