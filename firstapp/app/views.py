import hashlib
import random
import re
import time
import io
import os
import uuid
from _md5 import md5

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from django.core.paginator import Paginator
from django.core.serializers import json
from django.db.models import Q, Count
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.template import loader
from django.urls import reverse
from django.views.decorators.cache import cache_page

from app.models import Nav, Guest, Publishment, Announcement, Comment, CommentReply
from app.toolfunc import md5HashPwd, createVcode



# 首页
def index(request, pagenum=1):
    ptype = request.GET.get('ptype', None)
    # 根据帖子类型查询
    if ptype:
        publishment = Publishment.p_manager.filter(ptype=ptype).all().order_by('-paddtime')
        ptype = int(ptype)
    # 默认查询全部记录
    else:
        publishment = Publishment.p_manager.all().order_by('-paddtime')
    pager = Paginator(publishment, 5)
    pagePub = pager.page(pagenum)
    data = {
        'pagePub': pagePub,
        'pagerange': pager.page_range,
        'pagecount': pager.num_pages,
        'currentpage': pagePub.number,
        'ptype': ptype,
    }
    return render(request, 'app/index.html', context=data)


# 搜索
def search(request, pagenum):
    psearch = request.GET.get('psearch', None)
    publishment = Publishment.p_manager.filter(Q(ptitle__contains=psearch)).all().order_by('-paddtime')
    pager = Paginator(publishment, 3)
    pagePub = pager.page(pagenum)

    data = {
        'pagePub': pagePub,
        'pagerange': pager.page_range,
        'pagecount': pager.num_pages,
        'currentpage': pagePub.number,
        'psearch': psearch
    }
    # return render(request, 'app/search.html', context=data)
    template = loader.get_template('app/search.html')
    content = template.render(context=data)
    rere = re.compile(r'\*\*(.*)(' + psearch + r')(.*)\*\*')
    result, n = rere.subn(r'\1<span style="color:red;">\2</span>\3', content)
    return HttpResponse(result)


# 注册
def register(request):
    if request.method == 'GET':
        return render(request, 'app/register.html')
    else:
        post = request.POST
        gname = post.get('nickname', None)
        gemail = post.get('email', None)
        gpwd = post.get('pwd', None)
        ggender = post.get('gender', None)
        cpwd = post.get('cpwd', None)
        vcode = post.get('vcode', None)
        errcode = 0
        msg = ''
        res = ''

        # validate data
        if not gname or not gemail or not gpwd or not ggender or not cpwd or not vcode:
            res = 'fail'
            errcode = 1
            msg = '所有信息都要填!'
        elif vcode.lower() != request.session['vcode'].lower():
            res = 'fail'
            errcode = 1
            msg = '验证码错误!'
        elif gpwd != cpwd:
            res = 'fail'
            errcode = 1
            msg = '两次输入的密码不一样!'
        elif Guest.objects.filter(gname=gname).first():
            res = 'fail'
            errcode = 1
            msg = '昵称已存在'
        else:
            # hash pwd
            gpwd = md5HashPwd(gpwd.strip())

            # save data
            try:
                guest = Guest()
                guest.gname = gname.strip()
                guest.ggender = ggender.strip()
                guest.gemail = gemail.strip()
                guest.gpwd = gpwd
                guest.save()

                # genarate account
                g = Guest.objects.filter(gname=gname).first()
                gaccount = str(g.id + 1000)
                g.gaccount = gaccount
                g.save()
            except BaseException as e:
                res = 'fail'
                errcode = 2
                msg = '服务器出了点小问题。。。'
            else:
                res = 'ok'
                errcode = 0
                msg = '注册成功，您的账号是 ' + gaccount + '，清牢记！'

        return JsonResponse({
            'res': res,
            'errcode': errcode,
            'msg': msg
        })


# 登录
def login(request):
    if request.method == 'GET':
        return render(request, 'app/login.html')
    else:
        post = request.POST
        gaccount = post.get('account', None)
        gpwd = post.get('pwd', None)
        vcode = post.get('vcode', None)
        errcode = 0
        msg = ''
        res = ''
        if vcode.lower() != request.session['vcode'].lower():
            errcode = 1
            msg = '验证码错误!'
            res = 'fail'
        if gaccount and gpwd:
            # hash
            gpwd = md5HashPwd(gpwd)
            # validate
            g = Guest.objects.filter(gaccount=gaccount).first()
            if g and g.gpwd == gpwd:
                request.session['gname'] = g.gname
                request.session['gaccount'] = gaccount
                request.session['headphoto'] = 'uploads/' + g.gphoto.name
                errcode = 0
                msg = '登录成功!'
                res = 'ok'
            else:
                errcode = 1
                msg = '登录失败，账号或密码错误!'
                res = 'fail'
        else:
            errcode = 1
            msg = '所有参数都要填写!'
            res = 'fail'

        return JsonResponse({
            'res': res,
            'errcode': errcode,
            'msg': msg
        })


# 退出账号
def logout(request):

    request.session.flush()
    return render(request, 'app/logout.html')


# 个人信息
def myinfo(request):
    guest = Guest.objects.filter(gname=request.session.get('gname',None)).first()
    data = {
        'guest': guest,
        'gphoto': 'uploads/' + guest.gphoto.name
    }
    return render(request, 'app/myinfo.html', context=data)


# 获取验证码
def getVcode(request):
    vcodeinfo = createVcode(4)
    request.session['vcode'] = vcodeinfo[0]
    return HttpResponse(vcodeinfo[1], 'image/png')


# 更新密码
def modifypwd(request):
    errcode = 3
    msg = 'fail'
    res = '请求方法错误'
    if request.method == 'POST':
        gname = request.session.get('gname', None)
        oldpwd = request.POST.get('oldpwd', None)
        npwd = request.POST.get('npwd', None)
        cpwd = request.POST.get('cpwd', None)
        if not gname:
            errcode = 1
            msg = '尚未登录'
            res = 'fail'
        elif not oldpwd or not npwd or not cpwd:
            errcode = 1
            msg = '所有字段都是必填的！'
            res = 'fail'
        elif npwd != cpwd:
            errcode = 1
            msg = '两次输入的密码不一样！'
            res = 'fail'
        else:
            guest = Guest.objects.filter(gname=gname).first()
            if guest.gpwd != md5HashPwd(oldpwd.strip()):
                errcode = 1
                msg = '修改失败，原密码错误！'
                res = 'fail'
            else:
                try:
                    guest.gpwd = md5HashPwd(npwd.strip())
                    guest.save()
                except BaseException as e:
                    errcode = 2
                    msg = '服务器出了点问题。。。'
                    res = 'fail'
                else:
                    errcode = 0
                    msg = '修改成功！请尝试用新的密码登录！'
                    res = 'ok'
    return JsonResponse({
        'res': res,
        'errcode': errcode,
        'msg': msg
    })


# 设置头像
def setphoto(request):
    errcode = 3
    msg = 'fail'
    res = '请求方法错误'
    if request.method == 'POST':
        gname = request.session.get('gname', None)
        photo = request.FILES.get('photo', None)
        if not gname:
            errcode = 1
            msg = '尚未登录'
            res = 'fail'
        elif not photo:
            errcode = 1
            msg = '未上传任何图片'
            res = 'fail'

        else:
            try:
                photo.name = ''.join(str(uuid.uuid4()).split('-'))
                guest = Guest.objects.filter(gname=gname).first()
                guest.gphoto = photo
                guest.save()
            except BaseException as e:
                errcode = 2
                msg = '服务器出了点问题。。。'
                res = 'fail'
                print(e)
            else:
                errcode = 0
                msg = '头像设置成功！'
                res = 'ok'
    return JsonResponse({
        'res': res,
        'errcode': errcode,
        'msg': msg
    })


# 发布页面
@cache_page(60*60, cache='redis_cache')
def publishPage(request):
    return render(request, 'app/publish.html')


# 发布
def publish(request):
    errcode = 3
    msg = 'fail'
    res = '请求方法错误'
    if request.method == 'POST':
        gname = request.session.get('gname', None)
        post = request.POST
        ptitle = post.get('ptitle', None)
        ptype = post.get('ptype', None)
        pcontent = post.get('pcontent', None)
        if not gname:
            errcode = 1
            msg = '尚未登录'
            res = 'fail'
        elif not ptitle or not ptype or not pcontent:
            errcode = 1
            msg = '所有字段都是必填的！'
            res = 'fail'
        elif len(ptitle) > 20:
            errcode = 1
            msg = '标题太长了！'
            res = 'fail'
        else:
            pguest = Guest.objects.filter(gname=gname).first()
            ptype = Nav.n_manager.filter(id=ptype).first()

            try:
                publishment = Publishment()
                publishment.ptitle = ptitle
                publishment.pcontent = pcontent
                publishment.ptype = ptype
                publishment.pguest = pguest
                publishment.save()
            except BaseException as e:
                errcode = 2
                msg = '服务器出了点问题。。。'
                res = 'fail'
                print(e)
            else:
                errcode = 0
            msg = '发布成功！'
            res = 'ok'
    return JsonResponse({
        'res': res,
        'errcode': errcode,
        'msg': msg
    })


# 发布的内容详情
def detail(request, pubId):
    pub = Publishment.p_manager.all().filter(id=pubId).first()
    # 根据session判断是否点击过
    isclick = request.session.get('isclick' + pubId, None)
    print(isclick)
    if not isclick:
        pub.pclick = pub.pclick + 1
        pub.save()
        request.session['isclick' + pubId] = 1

    comment = Comment.objects.filter(cbelong=pubId).all()
    # print(comment)
    data = {
        'publish': pub,
        'comment': comment
    }
    return render(request, 'app/detail.html', context=data)


# 我的帖子
def myPublish(request, pagenum):
    gname = request.session.get('gname', None)
    if gname:
        guest = Guest.objects.filter(gname=gname).first()
        publishment = Publishment.p_manager.filter(pguest=guest).all()
        pager = Paginator(publishment, 4)
        pagePub = pager.page(pagenum)

        data = {
            'pagePub': pagePub,
            'pagerange': pager.page_range,
            'pagecount': pager.num_pages,
            'currentpage': pagePub.number,
        }
        return render(request, 'app/mypublish.html', context=data)
    else:
        return render(request, 'app/login.html')


# 编辑帖子
def editPublish(request, pubId):
    if request.method == 'POST':
        errcode = 0
        msg = ''
        res = ''
        gname = request.session.get('gname', None)
        post = request.POST
        ptitle = post.get('ptitle', None)
        ptype = post.get('ptype', None)
        pcontent = post.get('pcontent', None)
        if not gname:
            errcode = 1
            msg = '尚未登录'
            res = 'fail'
        elif not ptitle or not ptype or not pcontent:
            errcode = 1
            msg = '所有字段都是必填的！'
            res = 'fail'
        elif len(ptitle) > 20:
            errcode = 1
            msg = '标题太长了！'
            res = 'fail'
        elif not Publishment.p_manager.filter(id=pubId).first():
            errcode = 1
            msg = '帖子不存在！'
            res = 'fail'
        else:
            try:
                publishment = Publishment.p_manager.get(pk=pubId)
                publishment.ptitle = ptitle
                publishment.pcontent = pcontent
                publishment.ptype = Nav.n_manager.filter(id=ptype).first()
                publishment.save()
            except BaseException as e:
                errcode = 2
                msg = '服务器出了点问题。。。'
                res = 'fail'
                print(e)
            else:
                errcode = 0
                msg = '保存成功！'
                res = 'ok'
        return JsonResponse({
            'res': res,
            'errcode': errcode,
            'msg': msg
        })
    else:
        pub = Publishment.p_manager.get(pk=pubId)
        data = {
            'publish': pub,
            'pubId': pubId,
        }
        return render(request, 'app/editpublish.html', context=data)


# 公告详情
@cache_page(60*60, cache='redis_cache')
def announce(request, anId):
    announce = Announcement.a_manager.filter(id=anId).first()
    data = {
        'announce': announce,
    }
    return render(request, 'app/announcement.html', context=data)


# 删除帖子
def delPublish(request):
    errcode = 3
    msg = 'fail'
    res = '请求方法错误'
    if request.method == 'GET':
        pubId = request.GET.get('pubid', None)
        gname = request.session.get('gname', None)
        if not gname:
            errcode = 1
            msg = '尚未登录'
            res = 'fail'
        elif not pubId:
            errcode = 1
            msg = '参数缺失'
            res = 'fail'
        elif not Publishment.p_manager.filter(id=pubId).first():
            errcode = 1
            msg = '帖子不存在！'
            res = 'fail'
        else:
            try:
                publishment = Publishment.p_manager.get(pk=pubId)
                publishment.pisdelete = True
                publishment.save()
            except BaseException as e:
                errcode = 2
                msg = '服务器出了点问题。。。'
                res = 'fail'
                print(e)
            else:
                errcode = 0
                msg = '删除成功！'
                res = 'ok'
    return JsonResponse({
        'res': res,
        'errcode': errcode,
        'msg': msg
    })


# 评论帖子
def comment(request):
    errcode = 3
    msg = 'fail'
    res = '请求方法错误'
    if request.method == 'POST':
        gname = request.session.get('gname', None)
        ccontent = request.POST.get('ccontent', None)
        cbelong = request.POST.get('cbelong', None)

        if not gname:
            errcode = 1
            msg = '尚未登录'
            res = 'fail'
        elif not ccontent or not cbelong:
            errcode = 1
            msg = '参数缺失'
            res = 'fail'
        elif not Publishment.p_manager.filter(id=cbelong).all().first():
            errcode = 1
            msg = '帖子不存在'
            res = 'fail'
        else:
            try:
                cauthor = Guest.objects.filter(gname=gname).all().first()
                comment = Comment()
                comment.ccontent = ccontent
                comment.cbelong = Publishment.p_manager.filter(id=cbelong).all().first()
                comment.cauthor = cauthor
                comment.save()
            except BaseException as e:
                errcode = 2
                msg = '服务器出了点问题。。。'
                res = 'fail'
            else:
                errcode = 0
                msg = '评论成功！'
                res = 'ok'
    return JsonResponse({
        'res': res,
        'errcode': errcode,
        'msg': msg
    })

# 回复用户的评论
def replyComment(request):
    errcode = 3
    msg = 'fail'
    res = '请求方法错误'
    if request.method == 'POST':
        gname = request.session.get('gname', None)
        crcontent = request.POST.get('crcontent', None)
        crcomment = request.POST.get('crcomment', None)
        crto = request.POST.get('crto', None)
        if not gname:
            errcode = 1
            msg = '尚未登录'
            res = 'fail'
        elif not crcontent or not crcomment or not crto:
            errcode = 1
            msg = '参数缺失'
            res = 'fail'
        elif not Comment.objects.filter(id=crcomment).all().first():
            errcode = 1
            msg = '主评论不存在'
            res = 'fail'
        else:
            try:
                crauthor = Guest.objects.filter(gname=gname).all().first()
                commentreply = CommentReply()
                commentreply.crauthor = crauthor
                commentreply.crcontent = crcontent
                commentreply.crcomment = Comment.objects.filter(id=crcomment).all().first()
                commentreply.crto = Guest.objects.filter(id=crto).all().first()
                commentreply.save()
            except BaseException as e:
                errcode = 2
                msg = '服务器出了点问题。。。'
                res = 'fail'
            else:
                errcode = 0
                msg = '回复成功！'
                res = 'ok'
    return JsonResponse({
        'res': res,
        'errcode': errcode,
        'msg': msg
    })