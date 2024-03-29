# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-10-19 09:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FruitUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_username', models.CharField(max_length=32)),
                ('f_password', models.CharField(max_length=128, null=True)),
                ('f_age', models.IntegerField(default=0)),
                ('f_sex', models.BooleanField(default=False)),
                ('f_phone', models.CharField(max_length=32)),
                ('f_email', models.CharField(max_length=32)),
                ('f_icon', models.CharField(max_length=64, null=True)),
                ('f_ctime', models.DateTimeField(auto_now_add=True, null=True)),
                ('f_activated', models.BooleanField(default=False)),
                ('f_disabled', models.BooleanField(default=False)),
                ('f_delete', models.BooleanField(default=False)),
            ],
        ),
    ]
