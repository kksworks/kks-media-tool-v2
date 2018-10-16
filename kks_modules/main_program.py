#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
import torrent_auto_mgr

sys.setdefaultencoding("utf-8")

import threading
import time
 
def main_loop_torrent_run():
    print "thread : main_loop_torrent_run start"
    torrent_auto_mgr.run_torrent_down_all_site()
    print "thread : main_loop_torrent_run end"

def main_loop_torrent_thread_run():
    t1 = threading.Thread(target=main_loop_torrent_run)
    t1.daemon = True 
    t1.start()
    
if __name__ == "__main__":
    print "main script start"
    main_loop_torrent_run()
    print "main script end"

    #test_results  = torrent_auto_mgr.chk_parse_site(1);
    #for test_result in test_results :
    #    print "----------------------------"
    #    print "url : " + test_result['url']
    #    print "title : " + test_result['title']
    #    print "date : " + test_result['date']
    #    print "magnet : " + test_result['magnet']
    #    print "----------------------------"
    
    #torrent_auto_mgr.run_torrent_down_site_idx(3)

#print "test end?"

