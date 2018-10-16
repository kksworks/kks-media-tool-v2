#!/usr/bin/env python
#-*- coding: utf-8 -*-

# code by kksworks
# 본 프로그램은 사용자 과실에 대한 법적 책임을 지지 않습니다.

# licenses of python plugins
# python 2.6.11 이상사용
### beautifulsoup4 : MIT
### mechanize : BSD

from bs4 import BeautifulSoup
import mechanize, bencode
import time, os, hashlib, ConfigParser, ast, md5
import datetime
import shutil
import sys
import urllib
import subprocess

import urllib2
import ssl
import cookielib

import pymysql

import torrent_list_mgr
import torrent_site_mgr
import torrent_site_parser

import torrent_log


reload(sys)
sys.setdefaultencoding("utf-8")

genre_list = ["ent", "drama", "docu"]
MAX_FAIL_CHK_CNT = 10

def run_torrent_down_all_site() : 
	_torrent_down_target_site(0)

def run_torrent_down_site_idx(site_idx) : 
	_torrent_down_target_site(site_idx)

def _torrent_down_target_site(site_idx) : 
	torrent_log.debug_msg_print("run_torrent_down_all() start")

	torrent_log.log_save_normal__common("0", "common schedule : start");

	content_info_list = []

	# torrent list mgr
	torent_list_mgr = torrent_list_mgr.TorrentListMgr(0)
	torent_list_mgr.print_torrent_info()

	# torrent site mgr
	site_info_mgr = torrent_site_mgr.TorrentSiteMgr()
	site_info_mgr.print_site_info()

	site_info_list = site_info_mgr.get_site_list_idx(site_idx)

	if site_info_list == None :
		torrent_log.debug_msg_print("해당 사이트 없음 : site_idx => " + str(site_idx));
		return 

	for site_info in site_info_list : 
		parse_fail_cnt = 0
		content_info_list[:] = []
		for genre_name in genre_list:

			end_date = torent_list_mgr.chk_oldest_date(genre_name)

			for i in range(0, site_info['max_search_page']) : 

				if parse_fail_cnt > MAX_FAIL_CHK_CNT :
					torrent_log.debug_msg_print(" >> 사이트 응답없음 : 종료")
					break

				torrent_log.debug_msg_print("사이트 탐색시작 : " + str(i) + " / " + str(site_info['max_search_page']))
				parse_result = torrent_site_parser.read_content_by_site_info(site_info,genre_name,end_date, i, content_info_list) 

				if parse_result == "no-resp" : # 응닶없음
					parse_fail_cnt = parse_fail_cnt + 1
					site_info_mgr.update_fail_count_increase(site_info)
					torrent_log.log_save_err__torrent_site(str(site_info['id']), "사이트 응답없음")
					torrent_log.debug_msg_print("사이트 응답없음 : " + str(parse_fail_cnt));

				if parse_result == "err-date-invalid" : # 날짜 파싱안됨
					parse_fail_cnt = parse_fail_cnt + 1
					site_info_mgr.update_fail_count_increase(site_info)
					torrent_log.debug_msg_print("날짜데이터 파싱실패 : " + str(parse_fail_cnt));
					torrent_log.log_save_err__torrent_site(str(site_info['id']), "날짜데이터 파싱실패")

				site_info_mgr.update_parse_success(site_info)
				if parse_result == "pass-date" : # 날짜지남
					# torrent_log.log_save_normal__torrent_site(str(site_info['id']), "날짜지남");
					torrent_log.debug_msg_print("사이트 날짜 지남 ");
					break

			for content_info in content_info_list :
				torrent_id = torent_list_mgr.chk_valid_torrent_url(content_info['title'])
				if torrent_id is None :
					continue
				
				content_info['url'] = content_info['url'].replace("..", str(site_info['torrent_site']))

				magnet_text = torrent_site_parser.get_margnet_str(content_info['url'])
				if magnet_text is None :
					torrent_log.log_save_err__torrent_site(str(site_info['id']), "마그넷주소없음 : " + content_info['url'])
					continue

				torrent_log.debug_msg_print("found magnet : " + magnet_text)
				site_info_mgr.update_get_margnet_success(site_info)
				torrent_log.log_save_normal__torrent_site(str(site_info['id']), "마그넷주소 찾음 : " + magnet_text)
				torrent_log.debug_msg_print("found torrent magnet : " + magnet_text)
				magnet_add_ret = torent_list_mgr.torrent_magnet_add(torrent_id,magnet_text)
				if magnet_add_ret == True :
					torrent_log.log_save_normal__torrent_site(str(site_info['id']), "마그넷주소 추가 성공")
				else :
					torrent_log.log_save_normal__torrent_site(str(site_info['id']), "마그넷주소 추가 실패")
	
	torent_list_mgr.chk_torrent_list_after(0)
	
	torrent_log.log_save_normal__common("0", "common schedule : proram end")

	torrent_log.debug_msg_print("run_torrent_down_all() end")
	

def chk_parse_site(site_idx) : 
	torrent_log.debug_msg_print("run_torrent_chk() start ==> " + str(site_idx))
	
	content_info_list = []
	parse_result_list = []

	idx_target = int(site_idx)

	# torrent site mgr
	site_info_mgr = torrent_site_mgr.TorrentSiteMgr(True)
	#site_info_mgr.read_site_info()
	site_info_mgr.print_site_info()

	site_info  = site_info_mgr.get_site_list_idx(idx_target)

	if site_info == None :
		parse_result_0 = {
			'url' :  "null",
			'title' :  "null",
			'date' :  "null",
			'magnet' :  "해당사이트없음",
			#'tmp_to_download_flag' : False,
		}
		torrent_log.debug_msg_print("해당 사이트 없음 : site_idx => " + str(site_idx))
		parse_result_list.append(parse_result_0)
		return parse_result_list


	parse_fail_cnt = 0

	end_date =  datetime.date.today() - datetime.timedelta(days=30)

	for i in range(0, 7) : 
		torrent_log.debug_msg_print("test parsing start..")
		parse_result_0 = {
			'url' :  "null",
			'title' :  "null",
			'date' :  "null",
			'magnet' :  "null",
			#'tmp_to_download_flag' : False,
		}

		if parse_fail_cnt > 5 :
			torrent_log.debug_msg_print(" >> 파싱실패 : 종료")
			parse_result_0['magnet'] = "파싱실패 : 종료"
			parse_result_list.append(parse_result_0)
			return parse_result_list

		torrent_log.debug_msg_print("사이트 탐색시작 : " + str(site_info['max_search_page']))
		parse_result = torrent_site_parser.read_content_by_site_info(site_info, genre_list[0], end_date, 1, content_info_list) 

		if parse_result == "no-resp" : # 응닶없음
			parse_fail_cnt = parse_fail_cnt + 1
			torrent_log.debug_msg_print("사이트 응답없음 : " + str(parse_fail_cnt))
			parse_result_0['magnet'] = "사이트 응답없음..."
			parse_result_list.append(parse_result_0)
			continue

		if parse_result == "err-date-invalid" : # 날짜 파싱안됨
			parse_fail_cnt = parse_fail_cnt + 1
			torrent_log.debug_msg_print("날짜데이터 파싱실패 : " + str(parse_fail_cnt))
			parse_result_0['magnet'] = "날짜데이터 파싱실패..."
			parse_result_list.append(parse_result_0)
			continue
		
		max_test_cnt = len(content_info_list)
		if max_test_cnt > 5:
			max_test_cnt = 5

		for j in range(0, max_test_cnt) : 
			content_info = content_info_list[j]
			parse_result_1 = {
				'url' :  "null",
				'title' :  "null",
				'date' :  "null",
				'magnet' :  "null",
				#'tmp_to_download_flag' : False,
			}

			parse_result_1['url'] = content_info['url']
			parse_result_1['date'] = content_info['date']
			parse_result_1['title'] = content_info['title']

			
			content_info['url'] = content_info['url'].replace("..", str(site_info['torrent_site']))
			
			magnet_text = torrent_site_parser.get_margnet_str(content_info['url'])
			if magnet_text is None :
				torrent_log.log_save_err__torrent_site(str(site_info['id']), "마그넷주소없음 : " + content_info['url'])
				parse_result_1['magnet'] = "마그넷주소획득실패"
				continue
			
			torrent_log.log_save_normal__torrent_site(str(site_info['id']), "마그넷주소 찾음 : " + magnet_text)
			parse_result_list.append(parse_result_1)
			torrent_log.debug_msg_print("found magnet : " + magnet_text)
			parse_result_1['magnet'] = magnet_text

		torrent_log.debug_msg_print("found magnet : " + magnet_text)
		torrent_log.debug_msg_print("test parsing end..")
		return parse_result_list

	torrent_log.debug_msg_print("found torrent magnet : " + magnet_text)
	return parse_result_list
		
