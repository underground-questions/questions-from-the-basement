# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-21 20:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qna', '0004_auto_20160520_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='topic',
            field=models.CharField(max_length=25, unique=True),
        ),
    ]