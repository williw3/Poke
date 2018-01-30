# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-30 23:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poke',
            name='user',
        ),
        migrations.AddField(
            model_name='user',
            name='pokes',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]