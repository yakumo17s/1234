#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.conf.urls import url
from . import views
from .feeds import LatestPostsFeed


app_name = 'blog'
urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    # url(r'^$', views.PostListView.as_view(), name='post_list'),
    # (?P<year>)表示 year 参数, \d{4}表示数字 有4位,4位数字赋给 year.
    # [-\w]表示从符号'-'和\w表示的(字母,数字,下划线)中选择一个.
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.post_list, name="post_list_by_tag"),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'\
        r'(?P<post>[-\w]+)/$',
        views.post_detail,
        name='post_detail'),
    url(r'^(?P<post_id>\d+)/share/$', views.post_share,
        name='post_share'),
    url(r'^feed/$', LatestPostsFeed(), name='post_feed'),

]