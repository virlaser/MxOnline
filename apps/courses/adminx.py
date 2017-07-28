# coding:utf-8
import xadmin
import xlrd

from .models import Course, Lesson, Video, CourseResource, BannerCourse
from organization.models import CourseOrg


class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'go_to']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    # 排序
    ordering = ['-click_nums']
    # 只读字段
    readonly_fields = ['click_nums']
    # 不显示字段
    exclude = ['fav_nums']
    # 在添加课程的时候可以直接添加章节
    inlines = [LessonInline, CourseResourceInline]
    # 可以直接在列表页进行修改
    list_editable = ['degree', 'desc']
    # 列表刷新设置,选择3秒或者5秒
    refresh_time = [3, 5]
    # 富文本编辑器
    style_fields = {"detail": "ueditor"}
    # 从excel导入数据
    # import_excel = True

    # 把轮播课程和非轮播课程分别显示出来
    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    # 在添加课程的时候课程数量可以自己增长1
    def save_models(self):
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()

    # def post(self, request, *args, **kwargs):
    #     if 'excel' in request.FILES:
    #         pass
    #     return super(CourseAdmin, self).post(request, args, kwargs)

    # def post(self, request, *args, **kwargs):
    #     if 'excel' in request.FILES:
    #         # 初始化course
    #         course = Course()
    #         # 读取excel文件
    #         data = xlrd.open_workbook(request.FILES['excel'].name)
    #         # 获取excel第一个表
    #         table = data.sheets()[0]
    #         # 获取该表行数
    #         nrows = table.nrows
    #         # 第一行一般为表头，故从该表第二行开始循环取值
    #         for j in range(1, nrows):
    #             # 获取机构名称,根据表具体内容调整下标
    #             courseorg = table.row_values(j)[0]
    #             # 通过excel中机构名称中文向CourseOrg查询外键
    #             course.org_id = CourseOrg.objects.get(name=courseorg).id
    #             # 获取其他字段值,根据表具体内容调整下标
    #             course.name = table.row_values(j)[1]
    #             course.desc = table.row_values(j)[2]
    #             course.image = table.row_values(j)[3]
    #             # 保存数据
    #             course.save()
    #     return super(CourseAdmin, self).post(request, args, kwargs)


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    # 排序
    ordering = ['-click_nums']
    # 只读字段
    readonly_fields = ['click_nums']
    # 不显示字段
    exclude = ['fav_nums']
    # 在添加课程的时候可以直接添加章节
    inlines = [LessonInline, CourseResource]

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
