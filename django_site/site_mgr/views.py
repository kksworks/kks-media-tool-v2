# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
# Create your views here.

# Create your views here.
import datetime
import shutil
import time, os
import sys


from .models import TorrentSite
from .forms import TorrentSiteForm

import torrent_log
import torrent_auto_mgr

def main_views(request):
    return render(request, 'main.html')

def site_mgr_post_list(request):
    print "site_mgr_post_list req"
    site_mgrs = TorrentSite.objects.all()
    return render(request, 'site_mgr/post_list.html', {'torrent_sites': site_mgrs})

def site_mgr_post_edit(request, pk):
    if request.method == "POST":
        site_mgr = TorrentSite.objects.get(id=pk)
        form = TorrentSiteForm(request.POST,instance=site_mgr)
        if form.is_valid():
            post = form.save(commit=False)
            post.setting_file_chk = "file_need_to_check"
            post.save()
            return redirect('site_mgr_post_detail', pk=post.pk)
    else:
        torrent_info = TorrentSite.objects.get(id=pk)
        #my_record = TorrentList.objects.get(id=prog_name)
        form = TorrentSiteForm(instance=torrent_info)

    return render(request, 'site_mgr/post_edit.html', {'form': form})


def site_mgr_post_new(request):
    if request.method == "POST":
        form = TorrentSiteForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('site_mgr_post_detail', pk=post.pk)
    else:
        form = TorrentSiteForm()
    return render(request, 'site_mgr/post_new.html', {'form': form} )

def site_mgr_post_del(request, pk):
    site_mgr = get_object_or_404(TorrentSite, id=pk)
    
    if 'yes' in request.POST:
        site_mgr.delete()
        return redirect('site_mgr_post_list')
    elif 'no' in request.POST:
        return redirect('site_mgr_post_detail', pk=pk)
        
    if request.method == "POST":
        print "??????"
    else :
        return render(request, 'site_mgr/post_del.html', {'torrent_site': site_mgr})


def site_mgr_post_detail(request, pk):
	site_mgr = get_object_or_404(TorrentSite, id=pk)
	return render(request, 'site_mgr/post_detail.html', {'torrent_site': site_mgr})

def site_mgr_post_log(request, pk):
    log_lists = torrent_log.log_get__torrent_site(pk,60)
    return render(request, 'site_mgr/post_log.html', {'log_lists':log_lists})

def site_mgr_post_parse_test(request, pk):
    site_mgr = get_object_or_404(TorrentSite, id=pk)
    test_results = torrent_auto_mgr.chk_parse_site(pk)
    return render(request, 'site_mgr/post_parse_test.html', {'torrent_site': site_mgr, 'test_results': test_results})
