
#-*- coding: utf-8 -*-
from django import forms

from .models import TorrentSite

from django.utils import timezone
from django.forms.extras.widgets import SelectDateWidget
from django.forms import ModelForm, Form

import datetime

class TorrentSiteForm(forms.ModelForm):
    NUMBER_SEL = ( ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('0', '0'))
    NUMBER_SEL2 = ( ('10', '10'), ('20', '20'), ('40', '40'), ('70', '70'), ('100', '100'), ('130', '130'), ('200', '200') )
    NUMBER_SEL_RUN = ( ( '1', '실행'), ('0', '중지'))
    class Meta:
        model = TorrentSite
        fields = ('torrent_site1','is_use', 'content_table_total_row_cnt', 'content_table_chk_str', 'content_row_cnt_of_date', 'content_row_cnt_of_title', 'max_search_page', 'ent_url','drama_url','docu_url','url_page_prefix','url_page_suffix','date_format','date_format2','date_format3')
    
    torrent_site1 = forms.CharField(label='사이트주소', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    is_use = forms.ChoiceField(label='사용여부',choices=NUMBER_SEL_RUN,widget=forms.Select(attrs={'class':'form-control'}))
    content_table_total_row_cnt = forms.ChoiceField(label='컨텐츠 테이블 -> 열 갯수  (1 부터시작)',choices=NUMBER_SEL,widget=forms.Select(attrs={'class':'form-control'}))
    content_table_chk_str = forms.CharField(label='컨텐츠 테이블 -> 확인 문자열',widget=forms.TextInput(attrs={'class':'form-control'}))
    content_row_cnt_of_date = forms.ChoiceField(label='컨텐츠 테이블 -> 날짜 열 순서  (0 부터시작)',choices=NUMBER_SEL,widget=forms.Select(attrs={'class':'form-control'}))
    content_row_cnt_of_title = forms.ChoiceField(label='컨텐츠 테이블 -> 제목 열 순서  (0 부터시작)',choices=NUMBER_SEL,widget=forms.Select(attrs={'class':'form-control'}))
    max_search_page = forms.ChoiceField(label='최대 탐색페이지',choices=NUMBER_SEL2,widget=forms.Select(attrs={'class':'form-control'}))

    ent_url = forms.CharField(label='예능주소',widget=forms.TextInput(attrs={'class':'form-control'}))
    drama_url = forms.CharField(label='드라마주소',widget=forms.TextInput(attrs={'class':'form-control'}))
    docu_url = forms.CharField(label='시사교양주소',widget=forms.TextInput(attrs={'class':'form-control'}))

    url_page_prefix = forms.CharField(label='url_page_prefix',widget=forms.TextInput(attrs={'class':'form-control'}))
    url_page_suffix = forms.CharField(label='url_page_suffix',required = False, widget=forms.TextInput(attrs={'class':'form-control'}))

    date_format = forms.CharField(label='date_format first',widget=forms.TextInput(attrs={'class':'form-control'}))
    date_format2 = forms.CharField(label='date_format 2',required = False,widget=forms.TextInput(attrs={'class':'form-control'}))
    date_format3 = forms.CharField(label='date_format 3',required = False,widget=forms.TextInput(attrs={'class':'form-control'}))
    
