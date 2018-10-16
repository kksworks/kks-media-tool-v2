
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main_views, name='main_views'),
    url(r'^main/$', views.main_views, name='main_views'),
    url(r'^list/$', views.site_mgr_post_list, name='site_mgr_post_list'),
	url(r'^edit/(?P<pk>\d+)/$', views.site_mgr_post_edit, name='site_mgr_post_edit'),
    url(r'^new/$', views.site_mgr_post_new, name='site_mgr_post_new'),
    url(r'^detail/(?P<pk>\d+)/$', views.site_mgr_post_detail, name='site_mgr_post_detail'),
    url(r'^log/(?P<pk>\d+)/$', views.site_mgr_post_log, name='site_mgr_post_log'),
    url(r'^parse_test/(?P<pk>\d+)/$', views.site_mgr_post_parse_test, name='site_mgr_post_parse_test'),
]

