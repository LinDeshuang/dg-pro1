from django.db import models

# Create your models here.

# 访客
from tinymce.models import HTMLField


class Guest(models.Model):
    gname = models.CharField(max_length=20, null=False, unique=True, verbose_name='昵称')

    ggender = models.NullBooleanField(default=None, verbose_name='性别')

    gaccount = models.CharField(max_length=15, null=True, unique=True, verbose_name='账号')

    gemail = models.EmailField(null=False, verbose_name='邮箱')

    gpwd = models.CharField(max_length=50, null=False, verbose_name='密码')

    gphoto = models.ImageField(null=True, default='default.jpg', verbose_name='头像')

    gaddtime = models.DateTimeField(auto_now_add=True, verbose_name='注册日期')

    gisdelete = models.NullBooleanField(default=None, verbose_name='状态')

    def __str__(self):
        return self.gname

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = "用户"
        ordering = ['-gaddtime']


# 导航管理
class NavManager(models.Manager):

    def get_queryset(self):
        return super(NavManager, self).get_queryset().exclude(nisdelete=True)


class Nav(models.Model):
    nname = models.CharField(max_length=10, null=False, unique=True, verbose_name='命名')

    nsort = models.IntegerField(default=1, verbose_name='序号')

    naddtime = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    nstatus = models.IntegerField(default=1, verbose_name='状态')

    nisdelete = models.NullBooleanField(default=None, verbose_name='是否已删除')

    n_manager = NavManager()

    def __str__(self):
        return self.nname

    class Meta:
        verbose_name = '导航/帖子分类'
        verbose_name_plural = "导航/帖子分类"
        ordering = ['-naddtime']


# 发布管理
class PubManager(models.Manager):

    def get_queryset(self):
        return super(PubManager, self).get_queryset().order_by('-paddtime').exclude(pisdelete=True)


# 发布
class Publishment(models.Model):
    ptitle = models.CharField(max_length=30, null=False, verbose_name='标题')

    pcontent = HTMLField(null=False, verbose_name='内容')

    pclick = models.IntegerField(default=0, verbose_name='点击量')

    paddtime = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')

    pisdelete = models.NullBooleanField(default=None, verbose_name='是否删除')

    pisTop = models.IntegerField(default=0, verbose_name='是否置顶')

    pdetest = models.IntegerField(default=0, verbose_name='举报数量')

    pstatus = models.IntegerField(default=1, verbose_name='帖子状态')

    pguest = models.ForeignKey(Guest, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='发布者')

    ptype = models.ForeignKey(Nav, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='帖子类型')

    p_manager = PubManager()

    def __str__(self):
        return self.ptitle

    class Meta:
        verbose_name = '帖子'
        verbose_name_plural = "帖子"
        ordering = ['-paddtime']


# 评论或回答
class Comment(models.Model):
    ccontent = HTMLField(null=False, verbose_name='内容')

    cauthor = models.ForeignKey(Guest, related_name='user_comments', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='评论者')

    cbelong = models.ForeignKey(Publishment, related_name='art_comments', null=True, blank=True,
                                on_delete=models.SET_NULL,verbose_name='帖子')

    cstatus = models.BooleanField(default=True, verbose_name='状态')

    caddtime = models.DateTimeField(auto_now_add=True, verbose_name='发表时间')

    def __str__(self):
        return '{0}-{1}'.format(self.cauthor, self.caddtime.strftime("%Y-%m-%d %H:%M:%S"))

    class Meta:
        verbose_name = '帖子评论'
        verbose_name_plural = "帖子评论"
        ordering = ['-caddtime']


class CommentReply(models.Model):
    crcontent = HTMLField(null=False, verbose_name='内容')

    crcomment = models.ForeignKey(Comment, related_name='comment_replies', null=True, blank=True,
                                  on_delete=models.SET_NULL, verbose_name='主评论')

    crauthor = models.ForeignKey(Guest, related_name='user_comment_replies', null=True, blank=True,
                                 on_delete=models.SET_NULL, verbose_name='评论者')

    crto = models.ForeignKey(Guest, related_name='user_replied', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='被评论者')

    crstatus = models.BooleanField(default=True, verbose_name='状态')

    craddtime = models.DateTimeField(auto_now_add=True ,verbose_name='发表时间')

    def __str__(self):
        return '{0}->{1}'.format(self.crauthor, self.crto)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = "评论"
        ordering = ['-craddtime']


# 公告管理
class AnnManager(models.Manager):

    def get_queryset(self):
        return super(AnnManager, self).get_queryset().exclude(aisdelete=True)


# 公告
class Announcement(models.Model):
    atitle = models.CharField(max_length=30, null=False, verbose_name='标题')

    acontent = HTMLField(null=False, verbose_name='内容')

    aaddtime = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')

    astatus = models.IntegerField(default=1, verbose_name='状态')

    aisdelete = models.NullBooleanField(default=None, verbose_name='是否删除')

    a_manager = AnnManager()

    def __str__(self):
        return self.atitle

    class Meta:
        verbose_name = '公告'
        verbose_name_plural = "公告"
        ordering = ['-aaddtime']
