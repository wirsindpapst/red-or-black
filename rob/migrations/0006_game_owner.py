# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-03 17:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rob', '0005_auto_20170203_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='owner',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='rob.Player'),
        ),
    ]