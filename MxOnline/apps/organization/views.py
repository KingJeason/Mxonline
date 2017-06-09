# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import  View
from .models import  CourseOrg,CityDict,Teacher
from django.shortcuts import render_to_response
from .forms import UserAskForm
from django.http import HttpResponse
from operation.models import UserFavorite
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from courses.models import Course
# Create your views here.

class OrgView(View):
    def get(self,request):
        ##课程机构
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by('click_num')[:3 ]
        ##城市
        all_citys = CityDict.objects.all()
        # 取出筛选城市
        city_id = request.GET.get('city', "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 类别筛选
        catgory = request.GET.get('ct','')
        if catgory:
            all_orgs = all_orgs.filter(catgory = catgory)

        sort = request.GET.get('sort', "")
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by("-students")
            elif sort == 'courses':
                all_orgs = all_orgs.order_by("-course_nums")
        org_nums = all_orgs.count()
        ##对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 2,request=request)

        orgs = p.page(page)
        return render(request, 'org-list.html',{
            'all_orgs': orgs,
            'all_citys': all_citys,
            'org_nums': org_nums,
            'city_id': city_id,
            'catgory': catgory,
            'hot_orgs':hot_orgs,
            'sort': sort
        })

class AddUserAskView(View):
    ##用户添加咨询
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            ##直接保存到数据库
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"fuckingbitch"}', content_type='application/json')

class OrgCourseView(View):
    ## 课程页面
    def get(self, request, org_id):
        path = 'course'
        # 找到 organization下的CourseOrg这张表,然后读取机构id为org_id的程度
        course_org = CourseOrg.objects.get(id=int(org_id))
        ## 读取这个机构下的所有课程.
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'path':path,
            'has_fav':has_fav
        })

class OrgDescView(View):
    ## 机构首页
    def get(self, request, org_id):
        path = 'desc'
        # 找到 organization下的CourseOrg这张表,然后读取机构id为org_id的程度
        course_org = CourseOrg.objects.get(id=int(org_id))
        ## 读取这个机构下的所有课程.
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()[:2]
        all_teachers = course_org.teacher_set.all()[:2]
        return render(request, 'org-detail-desc.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'path': path,
            'has_fav':has_fav
        })

class OrgHomeView(View):
    ## 机构首页
    def get(self,request,org_id ):
        path = 'home'

        # 找到 organization下的CourseOrg这张表,然后读取机构id为org_id的程度

        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        ## 读取这个机构下的所有课程.
        all_courses = course_org.course_set.all()[:2]
        all_teachers = course_org.teacher_set.all()[:2]
        return render(request,'org-detail-homepage.html',{
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org':course_org,
            'path': path,
            'has_fav': has_fav
        })



class OrgTeachersView(View):
    ## 机构首页
    def get(self, request, org_id):
        path = 'teachers'
        # 找到 organization下的CourseOrg这张表,然后读取机构id为org_id的程度
        course_org = CourseOrg.objects.get(id=int(org_id))
        ## 读取这个机构下的所有课程.
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()[:2]
        all_teachers = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'path': path,
            'has_fav':has_fav
        })
class AddFavView(View):
    ## 用户收藏
    def post(self,request):
        fav_id = int(request.POST.get('fav_id',0))
        fav_type = int(request.POST.get('fav_type',0))
        ##首先判断用户是否登录
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')
        exist_records = UserFavorite.objects.filter(user = request.user,fav_id=fav_id,fav_type=fav_type )
        if exist_records:
            ##记录已经存在,则取消收藏
            exist_records.delete()
            return HttpResponse('{"status":"success","msg":"点击收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if fav_id> 0 and fav_type > 0:
                user_fav.user = request.user
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.save()
                return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":" fail"}', content_type='application/json')

class TeacherListView(View):
    ##课程讲师列表页
    def get(self,request):
        all_teachers = Teacher.objects.all()
        sort = request.GET.get('sort','')
        if sort:
            if sort == 'hot':
                all_teachers = all_teachers.order_by("-click_num")
        sorted_teacher = Teacher.objects.all().order_by('-click_num')[:3]
        ##对教师机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teachers, 1, request=request)

        teachers = p.page(page)
        return render(request, 'teachers-list.html',{
            'all_teachers': teachers,
            'sorted_teacher':sorted_teacher,
            'sort':sort
        })

class TeacherDetailView(View):
    def get(self,request,teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        all_courses = teacher.course_set.all()
        has_fav_teacher = False
        if UserFavorite.objects.filter(user=request.user,fav_type=3,fav_id=teacher.id):
            has_fav_teacher = True
        has_fav_org = False
        if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
            has_fav_org = True
        sorted_teacher = Teacher.objects.all().order_by('-click_num')[:3]
        return render(request, 'teacher-detail.html',{
            'teacher':teacher,
            'all_courses':all_courses,
            'sorted_teacher':sorted_teacher,
            'has_fav_teacher':has_fav_teacher,
            'has_fav_org':has_fav_org

        })