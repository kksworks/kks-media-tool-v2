# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-30 15:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TorrentList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prog_name', models.CharField(max_length=128)),
                ('prog_resol', models.CharField(max_length=128)),
                ('prog_rel_group', models.CharField(max_length=128)),
                ('prog_gene', models.CharField(max_length=128)),
                ('prog_date', models.CharField(max_length=64)),
                ('prog_date_interval', models.CharField(max_length=64)),
                ('prog_save_path', models.CharField(max_length=1024)),
                ('setting_file_chk', models.CharField(max_length=128)),
                ('setting_last_update_date', models.CharField(max_length=64)),
                ('setting_prog_max_save_date', models.CharField(max_length=64)),
                ('setting_reserved1', models.CharField(max_length=64)),
                ('setting_reserved2', models.CharField(max_length=64)),
                ('setting_reserved3', models.CharField(max_length=64)),
            ],
        ),
    ]