# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-30 23:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_mgr', '0003_auto_20171030_0919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='torrentsite',
            name='parse_fail_count',
            field=models.CharField(default='0', max_length=128),
        ),
    ]
