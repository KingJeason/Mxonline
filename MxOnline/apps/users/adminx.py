# _*_ coding:utf-8 _*_

import xadmin
from xadmin import  views
from .models import EmailVerifyRecord,UserProfile,Banner

## 全局配置

class BaseSetting(object):
    ## 主题配置
    enable_themes = True
    use_bootswatch = True

class GlobalSettings(object):
    ## 修改titele 和尾部 logo
    site_title = u'思源后台管理系统'
    site_footer = u'思源在线网'
    ## 左侧导航栏样式
    menu_style = "accordion"





class EmailVerifyRecordAdmin(object):
    list_display = ['code','email','send_type','send_time']
    search_fields = ['code','email','send_type']
    list_filter = ['code','email','send_type','send_time']

class UserProfileAdmin(object):
    pass

class BannerAdmin(object):
    list_display = ['title','image','url','index','add_time']
    search_fields = ['title','image','url','index']
    list_filter = ['title','image','url','index','add_time']

xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(UserProfile,UserProfileAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)

