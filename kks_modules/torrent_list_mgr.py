#!/usr/bin/env python
#-*- coding: utf-8 -*-
import datetime
import shutil
import time, glob, os
import sys
import subprocess

import pymysql

import torrent_log

reload(sys)
sys.setdefaultencoding("utf-8")

TRANSMISSION_ID = os.getenv('USER_CONF__TRANSMISSION_ID')
TRANSMISSION_PW = os.getenv('USER_CONF__TRANSMISSION_PW')

DB_INFO__TORRENT_LIST__ID = os.getenv('USER_CONF__DB_INFO__TORRENT_LIST__ID')
DB_INFO__TORRENT_LIST__PASS = os.getenv('USER_CONF__DB_INFO__TORRENT_LIST__PASS')
DB_INFO__TORRENT_LIST__DBNAME = os.getenv('USER_CONF__DB_INFO__TORRENT_LIST__DBNAME')
DB_INFO__TORRENT_LIST__TABLE = os.getenv('USER_CONF__DB_INFO__TORRENT_LIST__TABLE')

TORRENT_STR__FILE_NOT_EXIST = "file_not_exist"
TORRENT_STR__NEED_TO_CHK = "file_need_to_check"
TORRENT_STR__FILE_EXIST = "file_exist"

##############################
# torrent list mgr 
##############################
class TorrentListMgr:

	def __init__(self,idx):
		self.torent_list = []
		self.chk_torrent_list(idx)

	# ---------------------------------------------------------------------------------
	# torrent structure... 
	def get_torrent(self) :
		torrent_info = {
				'torrent_id' : 0,
				'torrent_name' :  "0",
				'torrent_date' : "000000",
				'torrent_date_interval' : "0",
				'torrent_resol' : "0",
				'torrent_rel' : "0",
				'torrent_genre' :  "0",
				'torrent_target_dir' : "0",

				'setting_file_checked' : "0",
				'setting_last_update_date' : "0",
				'setting_prog_max_save_date' : "0",

				#'tmp_to_download_flag' : False,
			}
		return torrent_info

	# ---------------------------------------------------------------------------------
	# read_torrent list config
	def read_torrent_info(self, idx) :

		self.clr_torrent()

		conn = pymysql.connect(host='localhost', user=DB_INFO__TORRENT_LIST__ID, password=DB_INFO__TORRENT_LIST__PASS, db=DB_INFO__TORRENT_LIST__DBNAME, charset='utf8')		
		curs = conn.cursor(pymysql.cursors.DictCursor)

		sql = "select * from {}".format(DB_INFO__TORRENT_LIST__TABLE)
		curs.execute(sql)

		rows = curs.fetchall()
		for row in rows:
			try:
				torrent_info = self.get_torrent()
				
				torrent_info['torrent_id'] = row['id']
				torrent_info['torrent_name'] = row['prog_name']
				torrent_info['torrent_date'] = row['prog_date']
				torrent_info['torrent_date_interval'] = row['prog_date_interval']
				torrent_info['torrent_resol'] = row['prog_resol'].lower()
				torrent_info['torrent_rel'] = row['prog_rel_group'].lower()
				torrent_info['torrent_genre'] = row['prog_gene'].lower()
				torrent_info['torrent_target_dir'] =row['prog_save_path']

				torrent_info['setting_file_checked'] = row['setting_file_chk']
				torrent_info['setting_last_update_date'] = row['setting_last_update_date']
				torrent_info['setting_prog_max_save_date'] = row['setting_prog_max_save_date']

				#torrent_info['tmp_to_download_flag'] = False
				if (idx > 0) and (torrent_info['torrent_id'] == idx) :
					self.torent_list.append(torrent_info)
				else :
					self.torent_list.append(torrent_info)

			except Exception, e:
				print "db qeury error : case 1"

		conn.close()

	# ---------------------------------------------------------------------------------
	def find_file_in_path_and_move(self, src_path, target_path) :
		for file_name in glob.glob(str(src_path)+'/*/*.mp4'):
			print file_name + " is checked!!!!!!!!!!!!!!!!!"
			shutil.move(file_name, target_path)
		for file_name in glob.glob(str(src_path)+'/*/*.mkv'):
			print file_name + " is checked!!!!!!!!!!!!!!!!!"
			shutil.move(file_name, target_path)
		for file_name in glob.glob(str(src_path)+'/*/*.avi'):
			print file_name + " is checked!!!!!!!!!!!!!!!!!"
			shutil.move(file_name, target_path)

	def fix_file_name_path(self, path) :
		for file in os.listdir(str(unicode(path))) :
                        full_filename = os.path.join(str(unicode(path)), str(file))
                        if os.path.isdir(full_filename) :
                                print full_filename + " is dir..."
				self.find_file_in_path_and_move(full_filename, str(unicode(path)))
				shutil.rmtree(full_filename, ignore_errors=True)
                        else :
				if file.find(' ') >= 0 : 
					print full_filename + " has space... remove space from file names.."
					file_rename = file.replace(" ","")
					shutil.move(full_filename, os.path.join(str(unicode(path)), str(file_rename)))
                                print full_filename + " is file.."

	def check_file_exist(self, path, date, name) :
		torrent_file_target_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
		torrent_file_target_date = torrent_file_target_date.strftime("%02y%02m%02d")

		self.fix_file_name_path(path)
		# torrent_log.debug_msg_print("check_file path : " + path + " ==> " + torrent_file_target_date)

		title_words = name.split(' ')
				
		for file in os.listdir(str(unicode(path))) :
			for title_word in title_words : 
				if not (file.find(title_word.decode("utf-8")) >= 0 ) :
					# torrent_log.debug_msg_print(" \t >> [file found] not found file name!!!")
					return False
			if file.find(torrent_file_target_date) >= 0 :
				# torrent_log.debug_msg_print( " \t >> [file found] found file success!!!")
				return True
			# check torrent name
				
		return False

	def delete_old_file(self, torrent_id, path, date) :
		dir_to_search = path
		now = time.time()
		if ( int(date) > 0 ) : 
			for dirpath, dirnames, filenames in os.walk(str(unicode(dir_to_search))):
				for file in filenames:
					curpath = os.path.join(str(unicode(dirpath)), str(unicode(file)))
					if os.stat(curpath).st_mtime < (now - int(date) * 24 * 60 * 60) :
						# torrent_log.debug_msg_print( "delete target is : " + curpath)
						torrent_log.log_save_normal__torrent_list(str(torrent_id), "delete target file : " + curpath);
						os.remove(str(unicode(curpath)))
			
	def chk_torrent_list_after(self,idx) : 
		self.read_torrent_info(idx)

		#torrent_log.log_save_normal__common("0", "chk_torrent_list_after : start");

		for cur_torrent_info in self.torent_list :
			# torrent_log.log_save_normal__torrent_list(str(cur_torrent_info['torrent_id']), "파일 확인 시작..");
			#torrent_log.log_save_normal__common("0", "common trace : 1");
			# 1. file path chk
			#if ( os.path.isdir(str(unicode(cur_torrent_info['torrent_target_dir']))) == False ) :
			#	os.makedirs(str(unicode(cur_torrent_info['torrent_target_dir'])));	
			#torrent_log.log_save_normal__common("0", "common trace : 2");
			# 2. last update vaild chk.
			try : 
				setting_last_update_date = datetime.datetime.strptime(cur_torrent_info['setting_last_update_date'], '%Y-%m-%d').date()
			except Exception, e:
				setting_last_update_date = datetime.date.today()
				self.update_torrent_last_update_day(cur_torrent_info['torrent_id'])
				
			
			torrent_file_target_date = datetime.datetime.strptime(cur_torrent_info['torrent_date'], '%Y-%m-%d').date()
			diff_today = (datetime.date.today() - torrent_file_target_date).days
			diff_last_update = (datetime.date.today() - setting_last_update_date).days

		
			# 2. too old torrent delete : chk 3 episode..
			if diff_last_update > ( int(cur_torrent_info['torrent_date_interval']) * 3 + 2) :
	 			# torrent_log.debug_msg_print( "debug : " + cur_torrent_info['torrent_name'] + " / 애피소드 3개 지났으므로 해당 토렌트리스트 삭제")
				torrent_log.log_save_normal__torrent_list(str(cur_torrent_info['torrent_id']), ">> AFTER CHK : 애피소드 3개 지났으므로 해당 토렌트리스트 삭제");
				#self.delete_torrent_info(cur_torrent_info['torrent_id'])
				#torrent_log.log_save_normal__torrent_list(str(cur_torrent_info['torrent_id']), "파일 확인 완료 : err case 1");
				continue

			# 3. skip empty episode..
			if diff_last_update > ( int(cur_torrent_info['torrent_date_interval']) + 2) :
				# torrent_log.debug_msg_print( "debug : " + cur_torrent_info['torrent_name'] + " / 에피소드 1개 지났으므로 다음 에피소드로..")
				torrent_log.log_save_normal__torrent_list(str(cur_torrent_info['torrent_id']), " >> AFTER CHK : 에피소드 1개 지났으므로 다음 에피소드로 : " + str(cur_torrent_info['torrent_date']));
				self.update_torrent_last_update_day(cur_torrent_info['torrent_id'])
				self.update_torrent_next_date(cur_torrent_info['torrent_id'])
				# torrent_log.log_save_normal__torrent_list(str(cur_torrent_info['torrent_id']), "파일 확인 완료 : err case 2");
				continue



			# cur_torrent_info['tmp_to_download_flag'] = True
			self.delete_old_file(cur_torrent_info['torrent_id'],cur_torrent_info['torrent_target_dir'],cur_torrent_info['setting_prog_max_save_date'])
			
			#self.update_torrent_chk_stat(cur_torrent_info['torrent_id'],  TORRENT_STR__FILE_NOT_EXIST)
			# torrent_log.log_save_normal__torrent_list(str(cur_torrent_info['torrent_id']), "파일 확인 완료 : normal");

		self.read_torrent_info(idx)

		#torrent_log.log_save_normal__common("0", "chk_torrent_list_after : end");

	def chk_torrent_list(self,idx) : 
		self.read_torrent_info(idx)

		for cur_torrent_info in self.torent_list :
			# torrent_log.log_save_normal__torrent_list(str(cur_torrent_info['torrent_id']), "파일 확인 시작..");
			#torrent_log.log_save_normal__common("0", "common trace : 1");
			# 1. file path chk
			if ( os.path.isdir(str(unicode(cur_torrent_info['torrent_target_dir']))) == False ) :
				os.makedirs(str(unicode(cur_torrent_info['torrent_target_dir'])));	
			#torrent_log.log_save_normal__common("0", "common trace : 2");
			# 2. last update vaild chk.
			try : 
				setting_last_update_date = datetime.datetime.strptime(cur_torrent_info['setting_last_update_date'], '%Y-%m-%d').date()
			except Exception, e:
				setting_last_update_date = datetime.date.today()
				self.update_torrent_last_update_day(cur_torrent_info['torrent_id'])
				
			
			torrent_file_target_date = datetime.datetime.strptime(cur_torrent_info['torrent_date'], '%Y-%m-%d').date()
			diff_today = (datetime.date.today() - torrent_file_target_date).days
			diff_last_update = (datetime.date.today() - setting_last_update_date).days

			# torrent_log.debug_msg_print(" -> debug : " + cur_torrent_info['torrent_name'] + " -> " + str(diff_today) + " / " + str(diff_last_update))
			if cur_torrent_info['setting_file_checked'] == TORRENT_STR__NEED_TO_CHK :
				# torrent_log.log_save_normal__torrent_list(str(cur_torrent_info['torrent_id']), "파일검사 시작 => 타겟날짜 : " + cur_torrent_info['torrent_date'] );
				if self.check_file_exist(cur_torrent_info['torrent_target_dir'], cur_torrent_info['torrent_date'], cur_torrent_info['torrent_name']) :
					torrent_log.log_save_normal__torrent_list(str(cur_torrent_info['torrent_id']), "폴더내 파일이 있습니다. : " + cur_torrent_info['torrent_date'] );

					# torrent_log.debug_msg_print("debug : " + cur_torrent_info['torrent_name'] + " / " + cur_torrent_info['torrent_date'] + " >>  파일이 폴더내에 파일이 있습니다.")
					self.update_torrent_last_update_day(cur_torrent_info['torrent_id'])
					self.update_torrent_next_date(cur_torrent_info['torrent_id'])
					torrent_log.log_save_normal__torrent_list(str(cur_torrent_info['torrent_id']), "파일 확인 완료 : 파일있음");
					continue

			# 3. current date chk..
			if diff_today < 0 :
				# torrent_log.debug_msg_print( "debug : 미래의 날짜입니다 ==> " + cur_torrent_info['torrent_name'] + "(" + cur_torrent_info['torrent_date'] + ")")
				# self.update_torrent_next_date(cur_torrent_info['torrent_id'])
				# torrent_log.log_save_normal__torrent_list(str(cur_torrent_info['torrent_id']), "미래의 날짜입니다 ==> (" + cur_torrent_info['torrent_date'] + ")");
				# torrent_log.log_save_normal__torrent_list(str(cur_torrent_info['torrent_id']), "파일 확인 완료 : 미래날짜.. skip");
				continue

			# 2. too old torrent delete : chk 3 episode..
			#if diff_last_update > ( int(cur_torrent_info['torrent_date_interval']) * 3 + 2) :
	 			# torrent_log.debug_msg_print( "debug : " + cur_torrent_info['torrent_name'] + " / 애피소드 3개 지났으므로 해당 토렌트리스트 삭제")
				#torrent_log.log_save_normal__torrent_list(str(cur_torrent_info['torrent_id']), "애피소드 3개 지났으므로 해당 토렌트리스트 삭제");
				#self.delete_torrent_info(cur_torrent_info['torrent_id'])
				# torrent_log.log_save_normal__torrent_list(str(cur_torrent_info['torrent_id']), "파일 확인 완료 : err case 1");
				#continue

			# 3. skip empty episode..
			#if diff_last_update > ( int(cur_torrent_info['torrent_date_interval']) + 2) :
				# torrent_log.debug_msg_print( "debug : " + cur_torrent_info['torrent_name'] + " / 에피소드 1개 지났으므로 다음 에피소드로..")
			#	torrent_log.log_save_normal__torrent_list(str(cur_torrent_info['torrent_id']), " >> 에피소드 1개 지났으므로 다음 에피소드로 : " + str(cur_torrent_info['torrent_date']));
				#self.update_torrent_next_date(cur_torrent_info['torrent_id'])
				# torrent_log.log_save_normal__torrent_list(str(cur_torrent_info['torrent_id']), "파일 확인 완료 : err case 2");
			#	continue

			# cur_torrent_info['tmp_to_download_flag'] = True
			#self.delete_old_file(cur_torrent_info['torrent_id'],cur_torrent_info['torrent_target_dir'],cur_torrent_info['setting_prog_max_save_date'])
			
			self.update_torrent_chk_stat(cur_torrent_info['torrent_id'],  TORRENT_STR__FILE_NOT_EXIST)
			# torrent_log.log_save_normal__torrent_list(str(cur_torrent_info['torrent_id']), "파일 확인 완료 : normal");

		self.read_torrent_info(idx)
	
	# ---------------------------------------------------------------------------------
	def clr_torrent(self) :
		while len(self.torent_list) != 0 :
			del self.torent_list[0]

	# ---------------------------------------------------------------------------------
	def print_torrent_info(self) : 
		# torrent_log.debug_msg_print( "torrent list info  ------------------------------------------- ")
#		for cur_torrent_info in self.torent_list :
			# torrent_log.debug_msg_print(str(cur_torrent_info['torrent_id']) +" -> "+ cur_torrent_info['torrent_name'] )
		 torrent_log.debug_msg_print("-------------------------------------------------------------- ")

	# ---------------------------------------------------------------------------------
	def chk_oldest_date(self, genre) :
		torrent_oldest_target_date = datetime.date.today() 
		torrent_oldest_target_name = "null"

		for cur_torrent_info in self.torent_list :
			torrent_file_target_date = datetime.datetime.strptime(cur_torrent_info['torrent_date'], '%Y-%m-%d').date()

			if (genre == cur_torrent_info['torrent_genre']) and (torrent_oldest_target_date >= torrent_file_target_date) :
				torrent_oldest_target_date = torrent_file_target_date
				torrent_oldest_target_name = cur_torrent_info['torrent_name']
		# torrent_log.debug_msg_print( "oldest file : " +  torrent_oldest_target_name + " >> " + torrent_oldest_target_date.strftime("%02y%02m%02d"))
		return torrent_oldest_target_date

	# ---------------------------------------------------------------------------------
	def chk_valid_torrent_url(self, title) :
		# #print "   - chk title :: " + title

		for cur_torrent_info in self.torent_list :
			# check torrent name
		#	#print "   - chk title :: " + title
		#	#print "   - target title :: " +  cur_torrent_info['torrent_name']
			found_title = True
			title_words = cur_torrent_info['torrent_name'].split(' ')

			for title_word in title_words : 
				if not (title.find(title_word.decode("utf-8")) >= 0) :
					found_title = False
					continue
			
			if found_title == False : 
				continue

			##print "   - chk title success :: " + cur_torrent_info['torrent_name'] + "/" + title
#			title_word = cur_torrent_info['torrent_name']

#			if not (title.find(title_word.decode("utf-8")) >= 0) :
#				continue
			
			# torrent date format yymmdd
			torrent_file_target_date = datetime.datetime.strptime(cur_torrent_info['torrent_date'], '%Y-%m-%d').date()
			torrent_file_target_date = torrent_file_target_date.strftime("%02y%02m%02d")

			if not (title.find(torrent_file_target_date.decode("utf-8")) >= 0 or cur_torrent_info['torrent_date'] == "*"):
				continue
		
			if not (title.find(cur_torrent_info['torrent_resol'].decode("utf-8")) >= 0 or cur_torrent_info['torrent_resol'] == "*"):
				continue
				
			if not (title.find(cur_torrent_info['torrent_rel'].decode("utf-8")) >= 0 or cur_torrent_info['torrent_rel'] == "*"):
				continue
			
			# 여기까지왔으면 찾은거다.

			#print "   - all chk success :: " + title + " >> " + str(cur_torrent_info['torrent_id'])
			torrent_log.log_save_normal__torrent_list(str(cur_torrent_info['torrent_id']), "게시물 확인완료 : title");
			return cur_torrent_info['torrent_id']
		
		# 하나도 없으므로..
		return None

	# ---------------------------------------------------------------------------------
	def get_torrent_info(self, torrent_id) :
		for cur_torrent_info in self.torent_list :
			if cur_torrent_info['torrent_id'] == torrent_id :
				return cur_torrent_info
		return None

	# ---------------------------------------------------------------------------------
	def update_torrent_next_date(self, torrent_id) :
		cur_torrent_info = self.get_torrent_info(torrent_id)
		if cur_torrent_info == None : 
			return False

		torrent_file_target_date = datetime.datetime.strptime(cur_torrent_info['torrent_date'], '%Y-%m-%d').date()
		torrent_file_target_date = torrent_file_target_date + datetime.timedelta(int(cur_torrent_info['torrent_date_interval']))
		
		

		cur_torrent_info['torrent_date'] = torrent_file_target_date.strftime("%04Y-%02m-%02d")
		cur_torrent_info['setting_file_checked'] = "file_need_to_check"

		torrent_log.log_save_normal__torrent_list(str(cur_torrent_info['torrent_id']), "skip target : " +  cur_torrent_info['torrent_date'] );

		self.update_torrent_info(torrent_id)

	# ---------------------------------------------------------------------------------
	def update_torrent_chk_stat(self, torrent_id, file_chk_stat) :
		cur_torrent_info = self.get_torrent_info(torrent_id)
		if cur_torrent_info == None : 
			return False

		cur_torrent_info['setting_file_checked'] = file_chk_stat
		self.update_torrent_info(torrent_id)

	# ---------------------------------------------------------------------------------
	def update_torrent_last_update_day(self, torrent_id) :
		cur_torrent_info = self.get_torrent_info(torrent_id)
		if cur_torrent_info == None : 
			return False

		setting_last_update_date = datetime.date.today()
		cur_torrent_info['setting_last_update_date'] = setting_last_update_date.strftime("%Y-%m-%d")

		self.update_torrent_info(torrent_id)

	# ---------------------------------------------------------------------------------
	def update_torrent_info(self, torrent_id) :
		cur_torrent_info = self.get_torrent_info(torrent_id)
		if cur_torrent_info == None : 
			return False

		conn = pymysql.connect(host='localhost', user=DB_INFO__TORRENT_LIST__ID, password=DB_INFO__TORRENT_LIST__PASS, db=DB_INFO__TORRENT_LIST__DBNAME, charset='utf8')
	
		curs = conn.cursor(pymysql.cursors.DictCursor)

		sql = """UPDATE {} SET 
				prog_date=%s, setting_file_chk=%s, setting_last_update_date=%s
				WHERE id = %s""".format(DB_INFO__TORRENT_LIST__TABLE)
				
	#	#print "db update qeury styr : " + sql
	#	#print  " >> id : " + str(cur_torrent_info['torrent_id'])
	#	#print  " >> update info " + cur_torrent_info['torrent_date'] + " , " + cur_torrent_info['setting_file_checked']
		
		curs.execute(sql, (cur_torrent_info['torrent_date'] , cur_torrent_info['setting_file_checked'], cur_torrent_info['setting_last_update_date'], str(cur_torrent_info['torrent_id'])))

		conn.commit()
		conn.close()

	def delete_torrent_info(self, torrent_id) :

		cur_torrent_info = self.get_torrent_info(torrent_id)
		if cur_torrent_info == None : 
			return False

		conn = pymysql.connect(host='localhost', user=DB_INFO__TORRENT_LIST__ID, password=DB_INFO__TORRENT_LIST__PASS, db=DB_INFO__TORRENT_LIST__DBNAME, charset='utf8')
	
		curs = conn.cursor(pymysql.cursors.DictCursor)

		sql = "DELETE FROM {} WHERE id = %s".format(DB_INFO__TORRENT_LIST__TABLE)
				
	#	#print "db update qeury styr : " + sql
	#	#print  " >> id : " + str(cur_torrent_info['torrent_id'])
	#	#print  " >> update info " + cur_torrent_info['torrent_date'] + " , " + cur_torrent_info['setting_file_checked']
		
		curs.execute(sql, (str(cur_torrent_info['torrent_id'])))

		torrent_log.log_save_normal__torrent_list(str(torrent_id),"Torrent Delete");

		conn.commit()
		conn.close()



	# ---------------------------------------------------------------------------------
	def torrent_magnet_add(self, torrent_id, magnet) :
		cur_torrent_info = self.get_torrent_info(torrent_id)
		if cur_torrent_info == None : 
			return False
		
		tm_id = TRANSMISSION_ID
		tm_pass = TRANSMISSION_PW
		path = str(unicode(cur_torrent_info['torrent_target_dir']))

		magnet = str(unicode(magnet))

		runcmd = "transmission-remote --auth %s:%s --add \"%s\" --download-dir \"%s\"" %(tm_id, tm_pass, magnet, path)
		
		runcmd = runcmd + "--torrent-done-script /home/torrent_mgr/tools/torrent_complete_tv_show.sh"

		p = subprocess.Popen(runcmd, stdout=subprocess.PIPE, shell=True)

		process_ret = p.stdout.read()
		
		#print "magnet add ret : " + process_ret
		if (process_ret.find("duplicate") >= 0) :
			self.update_torrent_last_update_day(torrent_id)
			self.update_torrent_next_date(torrent_id)
			torrent_log.log_save_normal__torrent_list(str(torrent_id), cur_torrent_info['torrent_name'] +" :: Torrent ADD Success : Duplicate ");
			return True
			
		if (process_ret.find("success") >= 0) :
			self.update_torrent_last_update_day(torrent_id)			
			self.update_torrent_next_date(torrent_id)
			torrent_log.log_save_normal__torrent_list(str(torrent_id), cur_torrent_info['torrent_name'] +" :: Torrent ADD Success");
			return True

		return False

