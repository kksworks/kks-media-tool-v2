# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.

class TorrentList(models.Model):
	# torernt_id = models.ForeignKey('auth.User')
	prog_name = models.CharField(max_length=128)
	prog_resol = models.CharField(max_length=128)
	prog_rel_group = models.CharField(max_length=128)
	prog_gene = models.CharField(max_length=128)
	prog_date = models.CharField(max_length=64)
	prog_date_interval = models.CharField(max_length=64)
	prog_save_path = models.CharField(max_length=1024)
	setting_file_chk = models.CharField(max_length=128)
	setting_last_update_date = models.CharField(max_length=64)
	setting_prog_max_save_date = models.CharField(max_length=64)
	setting_reserved1 = models.CharField(max_length=64)
	setting_reserved2 = models.CharField(max_length=64)
	setting_reserved3 = models.CharField(max_length=64)
	
	def publish(self):
		self.save()

	def __str__(self):
		return self.prog_name
