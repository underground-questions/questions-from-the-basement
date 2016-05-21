# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-20 19:40
from __future__ import unicode_literals

from django.db import migrations, models


def populate_tag_model(apps, schema_editor):
    Tag = apps.get_model("qna", "Tag")

    tag_topics = ['javascript', 'java', 'c#', 'python', 'git',
                  'other', 'ruby', 'html']

    for tag in tag_topics:
        t = Tag(topic=tag)
        t.save()


class Migration(migrations.Migration):

    dependencies = [
        ('qna', '0002_auto_20160519_2134'),
    ]

    operations = [
        migrations.RunPython(populate_tag_model),
    ]