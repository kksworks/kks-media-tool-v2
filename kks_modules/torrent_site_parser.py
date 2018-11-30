#!/usr/bin/env python
#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import mechanize, bencode
import time, os, hashlib, ConfigParser, ast, md5
import datetime
import shutil
import sys
import urllib

import urllib2
import ssl
import cookielib
import re

import torrent_log

"""
def set_browser_info():
	br = mechanize.Browser(factory=mechanize.RobustFactory())
	cj = mechanize.LWPCookieJar()
	br.set_cookiejar(cj)
	br.set_handle_equiv(True)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)
	br.set_handle_robots(False)
	br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
	br.addheaders = [("User-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4")]
	return br
"""


def get_content_by_url(url) :
	context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
			'Accept-Encoding': 'none',
			'Accept-Language': 'pl-PL,pl;q=0.8',
			'Connection': 'keep-alive'}

	cookiejar= cookielib.LWPCookieJar()
	opener= urllib2.build_opener( urllib2.HTTPCookieProcessor(cookiejar) )
	urllib2.install_opener(opener)
	req = urllib2.Request(url,None,hdr )
	try:
		page = urllib2.urlopen(req,context=context,timeout=3)
		
	except urllib2.HTTPError, e:
		return null;

	content = page.read()
	return content


def read_content_by_site_info(site_info, gene, end_date, page_no, content_info_list) :
	content_info_list_tmp = []

	target_url = site_info[gene + '_url'] + site_info['url_page_prefix'] + str(page_no) + site_info['url_page_suffix']

	table_total_row_cnt = site_info['content_table_total_row_cnt'] 
	table_chk_str = site_info['content_table_chk_str'] 

	row_cnt_of_date = site_info['content_row_cnt_of_date'] 
	row_cnt_of_title = site_info['content_row_cnt_of_title'] 


	try: 
		print " >> open target url : " + target_url
		doc_resp = get_content_by_url(target_url)
		#doc_resp = response.read()

		soup = BeautifulSoup(doc_resp, 'html.parser')
	except Exception, e:
		# print "\\n응답이 없습니다."
		torrent_log.log_save_err__torrent_site(str(site_info['id']),"응답이 없습니다. case 1 >> " + target_url);
		#sys.exit()
		return "no-resp"

	tables = soup.findAll("table")

	for table in tables:
		if table.findParent("table") is None:
			found_date = False
			tmp_chk_table = table.findAll(text=table_chk_str) 
			if len(tmp_chk_table) <= 0 :
				continue
			
			for row in table.findAll("tr"):
				cells = row.findAll("td")

				if not len(cells) == table_total_row_cnt:
					continue
				
				alink = cells[row_cnt_of_title].find("a")
				date_text = cells[row_cnt_of_date].get_text()

				if alink and date_text:
					content_info = {
						'title' : "null", 
						'url' : "null",
						'date' : "null",
					}
					tmp = alink.get_text()
					tmp = tmp.replace(" ", "")
					tmp = tmp.replace("\r", "")
					tmp = tmp.replace("\n", "")
					tmp = tmp.replace("\t", "")

					date_text = date_text.replace(" ", "")
					date_text = date_text.replace("\r", "")
					date_text = date_text.replace("\n", "")
					date_text = date_text.replace("\t", "")

					content_info['title'] = tmp.lower()
					content_info['url'] = alink["href"]
					print ">>> " + date_text

					if found_date == False : 
						try :
							target_date = datetime.datetime.strptime(date_text, site_info['date_format'] ).date()
							print "found date case 1" 
							found_date = True
						except Exception, e:
							found_date = False

					if found_date == False : 
						try :
							target_date = datetime.datetime.strptime(date_text, site_info['date_format2'] ).date()
							found_date = True
							print "found date case 2" 
						except Exception, e:
							found_date = False

					if found_date == False : 
						try :
							target_date = datetime.datetime.strptime(date_text, site_info['date_format3'] ).date()
							found_date = True
							print "found date case 3" 
						except Exception, e:
							found_date = False
					# 특정사이트의 경우 당일 게시물에 날짜형식이아니라 엉뚱한 스트링을 넣는다.
					if found_date == False : 
						if ( date_text.find('오늘') >= 0 or date_text.find('today') >= 0 ):
							target_date = datetime.date.today()
							found_date = True
							print "found date case 4" 
						else :
							found_date = False
	
					if found_date == False : 
						# return "err-date-invalid"
						target_date = datetime.date.today()
						print "found date case 5" 
						found_date == True 
					
					today_date = datetime.date.today()
					#print "diff date : " + str((today_date - target_date).days) 
					if target_date.year == 1900 and target_date.month == 1 and target_date.day == 1 :
						target_date = target_date.replace(year=today_date.year, month=today_date.month, day=today_date.day)
					elif target_date.year == 1900 :
						target_date = target_date.replace(year=today_date.year)
						
					content_info['date'] = target_date.strftime("%04Y-%02m-%02d")

					content_info_list.append(content_info)

	# print "   - last content : " + content_info['date'] + " >> " + content_info['title'] 
	# print "     -> url : "  + 	content_info['url'] 
	end_detect_date = end_date

	try :
		if target_date < end_detect_date : 
			return "pass-date"
		else :
			return "true"
	except Exception, e:
		return "pass-date"
		

def get_margnet_str(target_url) :
	print "   ->> chk marget target url : " + target_url

	try: 
		#response = br.open(torrent_info.torrent_target_url)
		response = get_content_by_url(target_url)
				
		soup = BeautifulSoup(response, 'html.parser')
	except Exception, e:
		#print "응답이 없습니다. : " + target_url
		torrent_log.log_save_err__torrent_site(str(site_info['id']),"응답이 없습니다. case 2 >> " + target_url);
		return None

	# for torrent kim
	get_values =  soup.find_all("input")
	for get_value in get_values:
		magnet_link = str(get_value.get('value'))
		if (magnet_link.find("magnet") >= 0) :
			return magnet_link

	get_values = soup.find_all("button")
	for get_value in get_values:
		magnet_link = str(get_value.get('onclick'))
		if (magnet_link.find("magnet_link(") >= 0) :
			return "magnet:?xt=urn:btih:" + magnet_link[13:-3]


	# normal site..
	get_links = soup.find_all("a")
	for get_link in get_links:
		magnet_link = str(get_link.get('href'))
		if (magnet_link.find("magnet") >= 0) :
			return magnet_link

	ifrmame_tags = soup.find_all('iframe')
	for ifrmame_tag in ifrmame_tags:
		print ifrmame_tag
		ifrmame_src = str(ifrmame_tag.get('src'))
		magnet_link = get_margnet_str(ifrmame_src)
		if magnet_link != None : 
			print magnet_link
			return magnet_link
	
	return None

def print_content_list(content_info_list) :
	print "--------------------------------------------------------"
	for content_info in content_info_list :
		print content_info['title'] + " : " + content_info['date'] +  " : " + content_info['url']
