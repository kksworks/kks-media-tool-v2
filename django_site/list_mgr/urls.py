
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main_views, name='main_views'),
    url(r'^main/$', views.main_views, name='main_views'),
    url(r'^list/$', views.list_mgr_post_list, name='list_mgr_post_list'),
    url(r'^detail/(?P<pk>\d+)/$', views.list_mgr_post_detail, name='list_mgr_post_detail'),
    url(r'^new/$', views.list_mgr_post_new, name='list_mgr_post_new'),
	url(r'^edit/(?P<pk>\d+)/$', views.list_mgr_post_edit, name='list_mgr_post_edit'),
    url(r'^del/(?P<pk>\d+)/$', views.list_mgr_post_del, name='list_mgr_post_del'),
    url(r'^log/(?P<pk>\d+)/$', views.list_mgr_log, name='list_mgr_log'),
]

