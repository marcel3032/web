# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-07-19 19:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiplomaDataSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Source name')),
                ('class_name', models.CharField(choices=[('file_upload', 'file_upload'), ('naboj_physics', 'naboj_physics'), ('naboj_math', 'naboj_math')], max_length=128, verbose_name='Source class')),
                ('is_default', models.BooleanField(default=False, verbose_name='Add to default sources')),
            ],
            options={
                'verbose_name': 'Data source for diplomas',
                'verbose_name_plural': 'Data sources for diplomas',
            },
        ),
        migrations.CreateModel(
            name='DiplomaTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('svg', models.TextField()),
                ('authorized_groups', models.ManyToManyField(blank=True, help_text='The groups that are authorized to use this template.', to='auth.Group', verbose_name='Authorized groups')),
                ('sources', models.ManyToManyField(blank=True, to='diplomas.DiplomaDataSource', verbose_name='Sources')),
            ],
            options={
                'verbose_name': 'Diploma template',
                'verbose_name_plural': 'Diploma templates',
            },
        ),
    ]
