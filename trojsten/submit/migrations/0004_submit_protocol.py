# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-07-08 16:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('old_submit', '0003_auto_20180701_2348'),
    ]

    operations = [
        migrations.AddField(
            model_name='submit',
            name='protocol',
            field=models.TextField(blank=True, null=True, verbose_name='protokol'),
        ),
    ]