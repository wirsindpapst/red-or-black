# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-05 20:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rob', '0022_remove_selection_lost_round'),
    ]

    operations = [
        migrations.AddField(
            model_name='selection',
            name='lost_round',
            field=models.IntegerField(blank=True, default=True),
        ),
    ]
