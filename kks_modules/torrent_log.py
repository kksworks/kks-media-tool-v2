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

#print os.environ['USER_CONF__DB_INFO__TORRENT_LOG__ID']
print '---------------------'
print os.getenv('USER_CONF__DB_INFO__TORRENT_LOG__ID')
print '---------------------'
DB_INFO__TORRENT_LOG__ID = os.getenv('USER_CONF__DB_INFO__TORRENT_LOG__ID')
DB_INFO__TORRENT_LOG__PASS = os.getenv('USER_CONF__DB_INFO__TORRENT_LOG__PASS')
DB_INFO__TORRENT_LOG__DBNAME = os.getenv('USER_CONF__DB_INFO__TORRENT_LOG__DBNAME')
DB_INFO__TORRENT_LOG__TABLE = os.getenv('USER_CONF__DB_INFO__TORRENT_LOG__TABLE')

def _log_save_common(log_type, log_id_1, log_id_2, log_process, log_content) :
    conn = pymysql.connect(host='localhost', user=DB_INFO__TORRENT_LOG__ID, password=DB_INFO__TORRENT_LOG__PASS, db=DB_INFO__TORRENT_LOG__DBNAME, charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)

    sql = """INSERT INTO {}
            (log_type, log_id_1, log_id_2, log_process, log_content)
            VALUES
            (%s,%s,%s,%s,%s)""".format(DB_INFO__TORRENT_LOG__TABLE)

    #	print "db update qeury styr : " + sql
    #	print  " >> id : " + str(cur_torrent_info['torrent_id'])
    #	print  " >> update info " + cur_torrent_info['torrent_date'] + " , " + cur_torrent_info['setting_file_checked']
        
    curs.execute(sql, (str(log_type), str(log_id_1), str(log_id_2), str(log_process), str(log_content) ))

    conn.commit()
    conn.close()

def log_save_err__torrent_list(log_id, log_content) :
    _log_save_common("ERR", "LIST_MGR"+log_id, 0, "LIST_MGR", log_content);

def log_save_warn__torrent_list(log_id, log_content) :
    _log_save_common("WARN", "LIST_MGR"+log_id, 0,  "LIST_MGR", log_content);

def log_save_normal__torrent_list(log_id, log_content) :
    _log_save_common("NORMAL", "LIST_MGR"+log_id, 0,  "LIST_MGR", log_content);

def log_save_err__torrent_site(log_id, log_content) :
    _log_save_common("ERR", "SITE_MGR"+log_id, 0,  "SITE_MGR", log_content);

def log_save_warn__torrent_site(log_id, log_content) :
    _log_save_common("WARN", "SITE_MGR"+log_id, 0,  "SITE_MGR", log_content);

def log_save_normal__torrent_site(log_id, log_content) :
    _log_save_common("NORMAL", "SITE_MGR"+log_id, 0,  "SITE_MGR", log_content);

def log_save_err__common(log_id, log_content) :
    _log_save_common("ERR", "COMMON"+log_id, 0,  "COMMON", log_content);

def log_save_warn__common(log_id, log_content) :
    _log_save_common("WARN", "COMMON"+log_id, 0,  "COMMON", log_content);

def log_save_normal__common(log_id, log_content) :
    _log_save_common("NORMAL", "COMMON"+log_id, 0,  "COMMON", log_content);

def _log_get__target_service(log_id, service, max_count) :
	log_lists = []
	conn = pymysql.connect(host='localhost', user=DB_INFO__TORRENT_LOG__ID, password=DB_INFO__TORRENT_LOG__PASS, db=DB_INFO__TORRENT_LOG__DBNAME, charset='utf8')
	curs = conn.cursor(pymysql.cursors.DictCursor)
	
	#sql = "select * from {} WHERE log_id_1 = %s OR log_process = 'COMMON'".format(DB_INFO__TORRENT_LOG__TABLE)
	#print "target id => " + str("LIST_MGR"+log_id)
	#print sql
	#curs.execute(sql, str("LIST_MGR"+log_id))

	#sql = "select * from {} WHERE log_id_1 = %s OR log_process = 'COMMON' LIMIT {}".format(DB_INFO__TORRENT_LOG__TABLE,max_count)
	sql = "select * from {} WHERE log_id_1 = %s ORDER BY `id` DESC LIMIT {}".format(DB_INFO__TORRENT_LOG__TABLE, int(max_count))

	print "target id => " + str(service+log_id)
	print sql
    
	curs.execute(sql, str(service+log_id))

	#sql = "select * from {}".format(DB_INFO__TORRENT_LOG__TABLE)
	#print sql
	#curs.execute(sql)

	rows = curs.fetchall()
	for row in rows:
		try:
			log_info = {
				'id' : u"null",
				'log_id_1' : u"null",
				'log_id_2' : u"null",
				'log_time' : u"null",
				'log_type' : u"null",
				'log_process' : u"null",
				'log_content' : u"null",
			}
		
			log_info['id'] = str(row['id'])
			log_info['log_id_1'] = row['log_id_1']
			log_info['log_id_2'] = row['log_id_2']
			log_info['log_time'] = str(row['log_time'])
			log_info['log_type'] = row['log_type']
			log_info['log_process'] = row['log_process']
			log_info['log_content'] = row['log_content']
		
			#torrent_info['tmp_to_download_flag'] = False
		
			log_lists.append(log_info)
		except Exception, e:
			print "db qeury error : case 33"

	return log_lists

def _log_get__target_service_2(service, max_count) :
    	log_lists = []
	conn = pymysql.connect(host='localhost', user=DB_INFO__TORRENT_LOG__ID, password=DB_INFO__TORRENT_LOG__PASS, db=DB_INFO__TORRENT_LOG__DBNAME, charset='utf8')
	curs = conn.cursor(pymysql.cursors.DictCursor)
	
	#sql = "select * from {} WHERE log_id_1 = %s OR log_process = 'COMMON'".format(DB_INFO__TORRENT_LOG__TABLE)
	#print "target id => " + str("LIST_MGR"+log_id)
	#print sql
	#curs.execute(sql, str("LIST_MGR"+log_id))

	#sql = "select * from {} WHERE log_id_1 = %s OR log_process = 'COMMON' LIMIT {}".format(DB_INFO__TORRENT_LOG__TABLE,max_count)
	sql = "select * from {} WHERE log_process = %s ORDER BY `id` DESC LIMIT {}".format(DB_INFO__TORRENT_LOG__TABLE, int(max_count))
	print sql
	curs.execute(sql, str(service))

	#sql = "select * from {}".format(DB_INFO__TORRENT_LOG__TABLE)
	#print sql
	#curs.execute(sql)

	rows = curs.fetchall()
	for row in rows:
		try:
			log_info = {
				'id' : u"null",
				'log_id_1' : u"null",
				'log_id_2' : u"null",
				'log_time' : u"null",
				'log_type' : u"null",
				'log_process' : u"null",
				'log_content' : u"null",
			}
		
			log_info['id'] = str(row['id'])
			log_info['log_id_1'] = row['log_id_1']
			log_info['log_id_2'] = row['log_id_2']
			log_info['log_time'] = str(row['log_time'])
			log_info['log_type'] = row['log_type']
			log_info['log_process'] = row['log_process']
			log_info['log_content'] = row['log_content']
		
			#torrent_info['tmp_to_download_flag'] = False
		
			log_lists.append(log_info)
		except Exception, e:
			print "db qeury error : case 33"

	return log_lists


def _log_get__target_service_3(max_count) :
	log_lists = []

	conn = pymysql.connect(host='localhost', user=DB_INFO__TORRENT_LOG__ID, password=DB_INFO__TORRENT_LOG__PASS, db=DB_INFO__TORRENT_LOG__DBNAME, charset='utf8')
	curs = conn.cursor(pymysql.cursors.DictCursor)
	
	#sql = "select * from {} WHERE log_id_1 = %s OR log_process = 'COMMON'".format(DB_INFO__TORRENT_LOG__TABLE)
	#print "target id => " + str("LIST_MGR"+log_id)
	#print sql
	#curs.execute(sql, str("LIST_MGR"+log_id))

	#sql = "select * from {} WHERE log_id_1 = %s OR log_process = 'COMMON' LIMIT {}".format(DB_INFO__TORRENT_LOG__TABLE,max_count)
	sql = "select * from {} WHERE 1 ORDER BY `id` DESC LIMIT {}".format(DB_INFO__TORRENT_LOG__TABLE, int(max_count))
	print sql
	curs.execute(sql)

	#sql = "select * from {}".format(DB_INFO__TORRENT_LOG__TABLE)
	#print sql
	#curs.execute(sql)

	rows = curs.fetchall()
	for row in rows:
		try:
			log_info = {
				'id' : u"null",
				'log_id_1' : u"null",
				'log_id_2' : u"null",
				'log_time' : u"null",
				'log_type' : u"null",
				'log_process' : u"null",
				'log_content' : u"null",
			}
		
			log_info['id'] = str(row['id'])
			log_info['log_id_1'] = row['log_id_1']
			log_info['log_id_2'] = row['log_id_2']
			log_info['log_time'] = str(row['log_time'])
			log_info['log_type'] = row['log_type']
			log_info['log_process'] = row['log_process']
			log_info['log_content'] = row['log_content']
		
			#torrent_info['tmp_to_download_flag'] = False
		
			log_lists.append(log_info)
		except Exception, e:
			print "db qeury error : case 33"

	return log_lists

def log_get__torrent_list(log_id, max_count) :
	return _log_get__target_service(log_id, "LIST_MGR", max_count) 

def log_get__torrent_site(log_id, max_count) :
	return _log_get__target_service(log_id, "SITE_MGR", max_count) 

def log_get__torrent_list_all(max_count) :
	return _log_get__target_service_2("LIST_MGR", max_count) 

def log_get__torrent_site_all(max_count) :
	return _log_get__target_service_2("SITE_MGR", max_count) 

def log_get__torrent_common_all(max_count) :
	return _log_get__target_service_2("COMMON", max_count) 

def log_get__all_msg(max_count) :
	return _log_get__target_service_3(max_count) 


def debug_msg_print(msg):
	start_time = time.time()
	now = time.localtime()
	msg_convert = str(unicode(msg))
	print "[%04d%02d%02d %02d:%02d:%02d] : " %(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec) + msg_convert

