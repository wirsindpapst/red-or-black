# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-03 18:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rob', '0006_game_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='colour',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
    ]