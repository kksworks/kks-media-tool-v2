#!/usr/bin/env python
#-*- coding: utf-8 -*-

import mechanize, bencode
import datetime
import shutil
import sys
import datetime
import shutil
import time, os
import sys

import pymysql

DB_INFO__TORRENT_SITE_INFO__ID = os.getenv('USER_CONF__DB_INFO__TORRENT_SITE_INFO__ID')
DB_INFO__TORRENT_SITE_INFO__PASS = os.getenv('USER_CONF__DB_INFO__TORRENT_SITE_INFO__PASS')
DB_INFO__TORRENT_SITE_INFO__DBNAME = os.getenv('USER_CONF__DB_INFO__TORRENT_SITE_INFO__DBNAME')
DB_INFO__TORRENT_SITE_INFO__TABLE = os.getenv('USER_CONF__DB_INFO__TORRENT_SITE_INFO__TABLE')


class TorrentSiteMgr:

	def __init__(self,forece_read=False):
		self.site_list = []
		self.content_list = []
		self.read_site_info(forece_read)

	# ---------------------------------------------------------------------------------
	# torrent structure... 
	def get_site(self) :
		site_info = {
				'id' : 0,
				'is_use' : '0',
				'torrent_site' : "null",
				'content_table_total_row_cnt' : 0,
				'content_table_chk_str' : "0",
				'content_row_cnt_of_date' : 0,
				'content_row_cnt_of_title' : 0,
				'max_search_page' : 0,
				'ent_url' : "null",
				'drama_url' : "null",
				'docu_url' : "null",
				'url_page_prefix' : "null",
				'url_page_suffix' : "null",
				'date_format' : "0",
				'date_format2' : "0",
				'date_format3' : "0",
				'last_success_date' : "0",
				'last_get_magnet_date' : "0",
				'parse_fail_count' : "0",
			}
		return site_info

	def get_site_list(self) :
		return self.site_list

	def get_site_list_idx(self, idx) :
		if idx <= 0 :
			return self.site_list

		for site_info in self.site_list:
			if site_info['id'] == idx : 
				return site_info
		return None

#	def get_site_list_one(self) : 
#		if len(self.site_list) != 0 :
#			site_info = self.site_list[0]
#			del self.site_list[0]
#			return site_info
#		else : 
#			return None

	def print_site_info(self) :
		print ""
		print "site info  ------------------------------------------- "
		for cur_site_info in self.site_list :
			print "id " + str(cur_site_info['id']) + " : " + cur_site_info['torrent_site']
		print "------------------------------------------------------"
		print ""

	def read_site_info(self, force_load=False) :
		conn = pymysql.connect(host='localhost', user=DB_INFO__TORRENT_SITE_INFO__ID, password=DB_INFO__TORRENT_SITE_INFO__PASS, db=DB_INFO__TORRENT_SITE_INFO__DBNAME, charset='utf8')		
		curs = conn.cursor(pymysql.cursors.DictCursor)

		sql = "select * from {}".format(DB_INFO__TORRENT_SITE_INFO__TABLE)
		
		curs.execute(sql)

		rows = curs.fetchall()
		for row in rows:
			try: 
				site_info = self.get_site()
				site_info['id'] = row['id']
				site_info['is_use'] = row['is_use']
				site_info['torrent_site'] = row['torrent_site1']

				site_info['content_table_total_row_cnt'] = int(row['content_table_total_row_cnt'])
				site_info['content_table_chk_str'] = row['content_table_chk_str']

				site_info['content_row_cnt_of_date'] = int(row['content_row_cnt_of_date'])
				site_info['content_row_cnt_of_title'] = int(row['content_row_cnt_of_title'])

				site_info['max_search_page'] = int(row['max_search_page'])

				site_info['ent_url'] = row['ent_url']
				site_info['drama_url'] = row['drama_url']
				site_info['docu_url'] = row['docu_url']

				site_info['url_page_prefix'] = row['url_page_prefix']
				site_info['url_page_suffix'] = row['url_page_suffix']
				
				site_info['date_format'] = row['date_format']
				site_info['date_format2'] = row['date_format2']
				site_info['date_format3'] = row['date_format3']

				site_info['last_success_date'] = row['last_success_date']
				site_info['last_get_magnet_date'] = row['last_get_magnet_date']
				site_info['parse_fail_count'] = row['parse_fail_count']


				if force_load == False :
					if  site_info['is_use'] == '1' :
						print "insert torrent site " + site_info['torrent_site'] 
						self.site_list.append(site_info)
				else:
					self.site_list.append(site_info)

			except Exception, e:
				print "db qeury error : case 1"

		conn.close()

#TODO: zzzzz fail debug
	def update_fail_count_increase(self, site_info) :
		target_id = site_info['id']

		target_fail_count = int(site_info['parse_fail_count']) + 1
		site_info['parse_fail_count'] = str(target_fail_count)

		conn = pymysql.connect(host='localhost', user=DB_INFO__TORRENT_SITE_INFO__ID, password=DB_INFO__TORRENT_SITE_INFO__PASS, db=DB_INFO__TORRENT_SITE_INFO__DBNAME, charset='utf8')		
	
		curs = conn.cursor(pymysql.cursors.DictCursor)

		sql = """UPDATE {} SET 
				parse_fail_count=%s
				WHERE id = %s""".format(DB_INFO__TORRENT_SITE_INFO__TABLE)
				
	#	print "db update qeury styr : " + sql
	#	print  " >> id : " + str(cur_torrent_info['torrent_id'])
	#	print  " >> update info " + cur_torrent_info['torrent_date'] + " , " + cur_torrent_info['setting_file_checked']
		
		curs.execute(sql, (str(target_fail_count), str(target_id)))

		conn.commit()
		conn.close()

		return target_fail_count

	def update_parse_success(self, site_info) :
		last_update_date = datetime.date.today()
		last_update_date = last_update_date.strftime("%Y-%m-%d")

		target_id = site_info['id']

		conn = pymysql.connect(host='localhost', user=DB_INFO__TORRENT_SITE_INFO__ID, password=DB_INFO__TORRENT_SITE_INFO__PASS, db=DB_INFO__TORRENT_SITE_INFO__DBNAME, charset='utf8')		
	
		curs = conn.cursor(pymysql.cursors.DictCursor)

		sql = """UPDATE {} SET 
				parse_fail_count=0, last_success_date=%s
				WHERE id = %s""".format(DB_INFO__TORRENT_SITE_INFO__TABLE)
				
	#	print "db update qeury styr : " + sql
	#	print  " >> id : " + str(cur_torrent_info['torrent_id'])
	#	print  " >> update info " + cur_torrent_info['torrent_date'] + " , " + cur_torrent_info['setting_file_checked']
		
		curs.execute(sql, (str(last_update_date), str(target_id)))

		conn.commit()
		conn.close()

	def update_get_margnet_success(self, site_info) :
		last_update_date = datetime.date.today()
		last_update_date = last_update_date.strftime("%Y-%m-%d")

		target_id = site_info['id']

		conn = pymysql.connect(host='localhost', user=DB_INFO__TORRENT_SITE_INFO__ID, password=DB_INFO__TORRENT_SITE_INFO__PASS, db=DB_INFO__TORRENT_SITE_INFO__DBNAME, charset='utf8')		
	
		curs = conn.cursor(pymysql.cursors.DictCursor)

		sql = """UPDATE {} SET 
				parse_fail_count=0, last_success_date=%s, last_get_magnet_date=%s
				WHERE id = %s""".format(DB_INFO__TORRENT_SITE_INFO__TABLE)
				
	#	print "db update qeury styr : " + sql
	#	print  " >> id : " + str(cur_torrent_info['torrent_id'])
	#	print  " >> update info " + cur_torrent_info['torrent_date'] + " , " + cur_torrent_info['setting_file_checked']
		
		curs.execute(sql, (str(last_update_date),str(last_update_date),str(target_id)))

		conn.commit()
		conn.close()

	def delete_torrent_site(self, site_id) :
    
		cur_site_info = self.get_site_list_idx(site_id)
		if cur_site_info == None : 
			return False

		conn = pymysql.connect(host='localhost', user=DB_INFO__TORRENT_SITE_INFO__ID, password=DB_INFO__TORRENT_SITE_INFO__PASS, db=DB_INFO__TORRENT_SITE_INFO__DBNAME, charset='utf8')
	
		curs = conn.cursor(pymysql.cursors.DictCursor)

		sql = "DELETE FROM {} WHERE id = %s".format(DB_INFO__TORRENT_LIST__TABLE)
				
	#	#print "db update qeury styr : " + sql
	#	#print  " >> id : " + str(cur_torrent_info['torrent_id'])
	#	#print  " >> update info " + cur_torrent_info['torrent_date'] + " , " + cur_torrent_info['setting_file_checked']
		
		curs.execute(sql, (str(cur_site_info['id'])))

		torrent_log.log_save_normal__torrent_list(str(torrent_id),"site info Delete");

		conn.commit()
		conn.close()
