# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-01-19 05:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0040_subcategoria_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoria',
            name='icono_seleccionado',
            field=models.FileField(blank=True, null=True, upload_to='static'),
        ),
    ]