# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-06-24 14:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Chainring', '0002_auto_20190624_2248'),
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='associated',
            name='userid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.EnterpriseCertificationInfo'),
        ),
    ]
