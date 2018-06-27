#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
页面的公共数据上下文渲染器
作为应用的context_processors

'''

# 获取导航分类
from django.db.models import Count

from app.models import Nav, Announcement, Publishment


def getNav():
    return Nav.n_manager.all().filter(nstatus=1).order_by('nsort')


# 获取公告信息
def getAnnouce():
    return Announcement.a_manager.all().filter(astatus=1).order_by('-aaddtime')


# 获取热评帖子
def getHotPub():
    return Publishment.p_manager.annotate(comments=Count('art_comments')).order_by('-comments').all()[0:5]


# 获取各页面共有数据
def getPublicData(request):
    return {
        'nav': getNav(),
        'annoucement': getAnnouce(),
        'hotpub': getHotPub(),
        'session': request.session,
    }