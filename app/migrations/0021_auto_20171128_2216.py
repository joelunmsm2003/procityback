# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-11-29 03:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_socia_descripcion_notificacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Configuracion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion_notificacion', models.CharField(blank=True, max_length=1000, null=True)),
            ],
            options={
                'verbose_name': 'Configuracion',
                'managed': True,
            },
        ),
        migrations.RemoveField(
            model_name='socia',
            name='descripcion_notificacion',
        ),
    ]