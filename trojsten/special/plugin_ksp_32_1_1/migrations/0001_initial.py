# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Try',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('input', models.CharField(max_length=15)),
                ('output', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='UserLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level_id', models.IntegerField()),
                ('try_count', models.IntegerField(default=0)),
                ('solved', models.BooleanField(default=False)),
                ('user', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='try',
            name='userlevel',
            field=models.ForeignKey(to='plugin_ksp_32_1_1.UserLevel'),
        ),
        migrations.AlterUniqueTogether(
            name='userlevel',
            unique_together=set([('user', 'level_id')]),
        ),
    ]
