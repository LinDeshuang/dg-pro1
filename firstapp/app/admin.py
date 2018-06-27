from django.contrib import admin

# Register your models here.
from app.models import Guest, Publishment, Announcement, Nav, Comment, CommentReply


class NavAdmin(admin.ModelAdmin):

    def getNstatus(self):
        if self.nstatus:
            return '正常'
        else:
            return '已禁用'

    list_display = ('nname', 'nsort', 'naddtime', getNstatus)


class GuestAdmin(admin.ModelAdmin):

    def getGender(self):
        if self.ggender == None:
            return '不详'
        elif self.ggender:
            return '男'
        else:
            return '女'

    def isDelete(self):
        if self.gisdelete == None:
            return '未删除'
        elif self.gisdelete:
            return '已删除'
        else:
            return '未删除'

    getGender.short_description = '性别'
    isDelete.short_description = '状态'

    list_display = ('gname', getGender, 'gphoto', 'gaccount', 'gemail', 'gaddtime', isDelete)


class PubAdmin(admin.ModelAdmin):
    list_display = ('ptitle', 'pclick', 'paddtime', 'pdetest', 'pguest', 'ptype')


class AnnAdmin(admin.ModelAdmin):
    list_display = ['atitle', 'aaddtime']




admin.site.site_header = '随便说'
admin.site.site_title = '随便说'
admin.site.register(Guest, GuestAdmin)
admin.site.register(Publishment, PubAdmin)
admin.site.register(Comment)
admin.site.register(CommentReply)
admin.site.register(Announcement,AnnAdmin)
admin.site.register(Nav, NavAdmin)
