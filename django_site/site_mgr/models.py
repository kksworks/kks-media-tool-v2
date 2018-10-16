# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.

class TorrentSite(models.Model):
    # torernt_id = models.ForeignKey('auth.User')
	torrent_site1 = models.CharField(max_length=128)
	is_use = models.CharField(max_length=128)
	content_table_total_row_cnt = models.CharField(max_length=128)
	content_table_chk_str = models.CharField(max_length=128)
	content_row_cnt_of_date = models.CharField(max_length=128)
	content_row_cnt_of_title = models.CharField(max_length=128)
	max_search_page = models.CharField(max_length=128)
	ent_url = models.CharField(max_length=128)
	drama_url = models.CharField(max_length=128)
	docu_url = models.CharField(max_length=128)
	url_page_prefix = models.CharField(max_length=128)
	url_page_suffix = models.CharField(max_length=128,blank=True, null=True)
	date_format = models.CharField(max_length=128)
	date_format2 = models.CharField(max_length=128)
	date_format3 = models.CharField(max_length=128)
	last_success_date = models.CharField(max_length=128)
	last_get_magnet_date = models.CharField(max_length=128)
	parse_fail_count = models.CharField(max_length=128,default='0')

	def publish(self):
		self.save()

	def __str__(self):
		return self.torrent_site
