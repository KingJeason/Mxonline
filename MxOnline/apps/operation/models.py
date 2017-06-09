# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import  datetime

from django.db import models

from users.models import UserProfile
from courses.models import Course

# Create your models here.


class UserAsk(models.Model):
    name = models.CharField(max_length=20,verbose_name=u'姓名')
    mobile =models.CharField(max_length=11,verbose_name=u'手机')
    course_name = models.CharField(max_length=50,verbose_name=u'课程')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户咨询'
        verbose_name_plural = verbose_name

class CourseComments(models.Model):
    ## 课程评论
    user = models.ForeignKey(UserProfile, verbose_name=u'用户')
    course = models.ForeignKey(Course, verbose_name=u'课程')
    comments = models.CharField(max_length=200,default='',verbose_name=u'评论')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')


    class Meta:
        verbose_name = u'课程评论'
        verbose_name_plural = verbose_name


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u'用户')
    fav_id = models.IntegerField(default=0, verbose_name=u'数据id')
    fav_type = models.IntegerField(choices=((1,'课程'),(2,'课程机构'),(3,'讲师')),default=1,verbose_name=u'收藏类型')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户收藏'
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    ## 当user等于0时,默认给所有人发送消息,当user等于其他数字时,即是给id为这个数字的user发消息(这里不能用外键,因为没法给所有人发送消息)
    user = models.IntegerField(default=0,verbose_name=u'接收用户')
    message = models.CharField(max_length=500,verbose_name=u'消息内容')
    has_read = models.BooleanField(default=False,verbose_name=u'是否已读')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'发送时间')


    class Meta:
        verbose_name = u'用户消息'
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u'用户')
    course = models.ForeignKey(Course, verbose_name=u'课程')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户课程'
        verbose_name_plural = verbose_name


