
#-*- coding: utf-8 -*-
from django import forms

from .models import TorrentList

from django.utils import timezone
from django.forms.extras.widgets import SelectDateWidget
from django.forms import ModelForm, Form

import datetime

class TorrentListForm(forms.ModelForm):
    TORRENT_GENRES = (('ent', 'ent'), ('drama', 'drama'), ('docu', 'docu'))
    TORRENT_RESOL = ( ('720p', '720p'), ('1080p', '1080p'), ('*', '*'))
    TORRENT_REL_GROUP = ( ('next', 'next'), ('cinebus', 'cinebus'), ('*', '*'))
    TORRENT_INTERVAL = ( ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'))
    TORRENT_MAX_SAVE_DAY = ( ('0', '0'), ('60', '60'), ('120', '120'), ('180', '180') )
    DOY = ('2017', '2018', '2019')

    class Meta:
        model = TorrentList
        fields = ('prog_name', 'prog_resol', 'prog_rel_group', 'prog_gene', 'prog_date', 'prog_date_interval', 'prog_save_path','setting_prog_max_save_date',)
    
    prog_name = forms.CharField(label='프로그램이름', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    prog_gene = forms.ChoiceField(label='장르 설정',choices=TORRENT_GENRES,widget=forms.Select(attrs={'class':'form-control'}))
    prog_rel_group = forms.ChoiceField(label='릴그룹',choices=TORRENT_REL_GROUP,widget=forms.Select(attrs={'class':'form-control'}))
    prog_resol = forms.ChoiceField(label='해상도',choices=TORRENT_RESOL,widget=forms.Select(attrs={'class':'form-control'}))
    prog_date = forms.DateField(label='프로그램 날짜', widget = forms.SelectDateWidget(years = DOY,attrs={'class':'form-control'}), initial = timezone.now)
    prog_date_interval = forms.ChoiceField(label='프로그램 확인주기',choices=TORRENT_INTERVAL, initial='7',widget=forms.Select(attrs={'class':'form-control'}))
    prog_save_path = forms.CharField(label='프로그램 저장경로', initial = '/mnt/5T_1_media_disk/pub/tv/예능프로그램/',widget=forms.TextInput(attrs={'class':'form-control'}))
    setting_prog_max_save_date = forms.ChoiceField(label='최대저장일',choices=TORRENT_MAX_SAVE_DAY, initial='180',widget=forms.Select(attrs={'class':'form-control'}))

