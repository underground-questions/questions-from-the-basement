# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-18 19:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qna', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='owner',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]
