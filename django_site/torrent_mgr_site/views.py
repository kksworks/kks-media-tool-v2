# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect

# Create your views here.
import datetime
import shutil
import time, os
import sys

import torrent_log

import main_program

def main_views(request):
    print "dddd?D?"
    if 'run torrent' in request.POST:
        main_program.main_loop_torrent_thread_run()
    return render(request, 'main.html')


def log_views(request):
    log_lists = torrent_log.log_get__all_msg(400)
    return render(request, 'main_log.html', {'log_lists':log_lists})

