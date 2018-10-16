"""torrent_mgr_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.main_views, name='main_views'),
    url(r'main', views.main_views, name='main_views'),
    url(r'all_log', views.log_views, name='log_views'),
    url(r'^admin/', admin.site.urls),
    url(r'^list_mgr/', include('list_mgr.urls')),
    url(r'^site_mgr/', include('site_mgr.urls')),
]
