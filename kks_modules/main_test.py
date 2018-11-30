#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
import torrent_auto_mgr
import main_program
sys.setdefaultencoding("utf-8")

import threading
import time

if __name__ == "__main__":
    print "main script start"
#    torrent_auto_mgr.run_torrent_down_all_site()
    print "main script end"

    #test_results  = torrent_auto_mgr.chk_parse_site(1);
    #for test_result in test_results :
    #    print "----------------------------"
    #    print "url : " + test_result['url']
    #    print "title : " + test_result['title']
    #    print "date : " + test_result['date']
    #    print "magnet : " + test_result['magnet']
    #    print "----------------------------"
    
#    torrent_auto_mgr.chk_parse_site(5)
    main_program.main_loop_torrent_run()

#print "test end?"

