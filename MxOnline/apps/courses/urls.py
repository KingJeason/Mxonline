# _*_ coding: utf-8 _*_
__author__ = 'Jeason'
__date__ = '2017/4/30 0:18'

from django.conf.urls import url,include
from .views import CourseView,CourseDetailView,CourseCommentView,CourseVideoView,AddCommentView



urlpatterns =[
    ##课程机构首页
    url(r'^list/$', CourseView.as_view(), name='course_list'),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name='course_comment'),
    url(r'^video/(?P<course_id>\d+)/$', CourseVideoView.as_view(), name='course_video'),
    url(r'^add_comment', AddCommentView.as_view(), name='add_comment'),
]