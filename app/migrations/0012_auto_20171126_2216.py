# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-11-26 22:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20171126_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turnosocia',
            name='dia',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Dia'),
        ),
    ]
