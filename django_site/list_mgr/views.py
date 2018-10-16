# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect

# Create your views here.
import datetime
import shutil
import time, os
import sys

from .models import TorrentList
from .forms import TorrentListForm

import torrent_log

reload(sys) 
sys.setdefaultencoding('utf-8')

def main_views(request):
    return render(request, 'main.html')

# Create your views here.
def list_mgr_post_list(request):
    list_mgrs = TorrentList.objects.all()
    return render(request, 'list_mgr/post_list.html', {'torrent_lists': list_mgrs})

def list_mgr_post_detail(request, pk):
    torrent_info = get_object_or_404(TorrentList, id=pk)
    # log_mgr = TorrentLogMgr()
    # log_lists = torrent_log.log_get__torrent_list(pk,60)
    filesystem_list = []
    dir_to_search = torrent_info.prog_save_path
    for dirpath, dirnames, filenames in os.walk(str(unicode(dir_to_search))):
            for file in filenames:
                curpath = os.path.join(dirpath, file)
                filesystem_list.append(curpath)
    return render(request, 'list_mgr/post_detail.html', {'torrent_info': torrent_info,'filesystem_list':filesystem_list})

def list_mgr_post_del(request, pk):
    torrent_info = get_object_or_404(TorrentList, id=pk)
    if 'yes' in request.POST:
        torrent_info.delete()
        return redirect('list_mgr_post_list')
    elif 'no' in request.POST:
        return redirect('list_mgr_post_detail', pk=pk)
        
    if request.method == "POST":
        print "list_mgr_post_del - run post"
    else :
        return render(request, 'list_mgr/post_del.html', {'torrent_info': torrent_info})

def list_mgr_post_edit(request, pk):
    if request.method == "POST":
        torrent_info = TorrentList.objects.get(id=pk)
        form = TorrentListForm(request.POST,instance=torrent_info)
        if form.is_valid():
            post = form.save(commit=False)
            post.setting_file_chk = "file_need_to_check"
            post.save()
            return redirect('list_mgr_post_detail', pk=post.pk)
    else:
        torrent_info = TorrentList.objects.get(id=pk)
        #my_record = TorrentList.objects.get(id=prog_name)
        form = TorrentListForm(instance=torrent_info)

    return render(request, 'list_mgr/post_edit.html', {'form': form})

def list_mgr_post_new(request):
    if request.method == "POST":
        form = TorrentListForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.setting_file_chk = "file_need_to_check"
            post.save()
            return redirect('list_mgr_post_detail', pk=post.pk)
    else:
        form = TorrentListForm()
    return render(request, 'list_mgr/post_new.html', {'form': form} )

def list_mgr_log(request, pk):
    # log_mgr = TorrentLogMgr()
    log_lists = torrent_log.log_get__torrent_list(pk,60)
    return render(request, 'list_mgr/post_log.html', {'log_lists':log_lists})


