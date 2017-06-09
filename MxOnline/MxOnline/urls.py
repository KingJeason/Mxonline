# _*_ coding:utf-8 _*_
"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url,include
##from django.contrib import admin
## 专门处理静态html 文件
from  django.views.generic import  TemplateView
from users.views import LoginView,RegisterView,AciveUserView,ForgetPwdView,ResetView,ModifyPwdView
from organization.views import OrgView
from django.views.static import serve
import xadmin
from MxOnline.settings import MEDIA_ROOT
urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='index.html'),name='index'),
    url(r'^login/$',LoginView.as_view(), name='login'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$',AciveUserView.as_view(),name='user_active'),
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name='reset_pwd'),
    url(r'^modify_pwd/$',ModifyPwdView.as_view(),name="modify_pwd"),
    ##课程机构
    url(r'^org/',include('organization.urls',namespace='org')),
    ###  课程
    url(r'^course/', include('courses.urls', namespace='course')),
    ##配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve,{'document_root':MEDIA_ROOT})

]
