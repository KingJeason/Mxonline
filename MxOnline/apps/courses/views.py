# _*_ coding: utf-8 _*_
from django.shortcuts import render
from django.views.generic import  View
from .models import Course,CourseResource
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
from operation.models import CourseComments
from django.http import HttpResponse
from operation.models import UserFavorite,UserCourse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from utils.mixin_utils import LoginRequiredMixin
# Create your views here.
class CourseView(View):
    def get(self,request):
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]
        sort = request.GET.get('sort','')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by("-students")
            elif sort == 'hot':
                all_courses = all_courses.order_by("-click_nums")
        ## 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 3, request=request)

        courses = p.page(page)
        return render(request,'course-list.html',{
            'all_courses':courses,
            'sort':sort,
            'hot_courses':hot_courses
        })


class CourseDetailView(View):
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()
        tag = course.tag
        ##判断是否收藏
        has_fav = False
        has_fav1 = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav1 = True

        if tag:
            relate_coures = Course.objects.filter(tag=tag).order_by('-click_nums')[:1]
        else:
            relate_coures = []
        return render(request,'course-detail.html',{
            'course':course,
            'relate_coures':relate_coures,
            'has_fav':has_fav,
            'has_fav1':has_fav1
        })


class CourseCommentView(View):
    def get(self, request, course_id):
        select = 'comment'
        course = Course.objects.get(id=int(course_id))
        all_resource = CourseResource.objects.filter(course=course)
        all_comment = CourseComments.objects.filter(course=course)
        return render(request, 'course-comment.html', {
            'course': course,
            'all_resource': all_resource,
            'all_comment': all_comment,
            'select':select
        })


class CourseVideoView(LoginRequiredMixin,View):
    def get(self, request, course_id):
        select = 'video'
        course = Course.objects.get(id=int(course_id))
        ##查询当前用户是否学习了此课程

        user_courses = UserCourse.objects.filter(user=request.user,course=course)
        ## 若没有学习,则改变其状态,保存在数据库中
        if not user_courses:
            user_course = UserCourse(user=request.user,course=course)
            user_course.save()
            ## 取出数据库中课程为course的数据 可能有多个数据
        user_courses = UserCourse.objects.filter(course=course)
        ##取出学过这门课程的用户的id
        user_ids = [user_course.user.id for user_course in user_courses]
        ##取出所有课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        ##取出所有课程id
        course_ids = [user_couser.course.id for user_couser in all_user_courses]

        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]
        all_resource = CourseResource.objects.filter(course=course)

        return render(request,'course-video.html',{
            'course': course,
            'all_resource':all_resource,
            'select':select,
            'relate_courses':relate_courses

        })


class AddCommentView(LoginRequiredMixin,View):
    def post(self,request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')

        course_id = request.POST.get('course_id',0)
        comments = request.POST.get('comments','')
        if course_id > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments  = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success","msg":"发表成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加失败"}', content_type='application/json')
