# coding:utf-8
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
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve
import xadmin

from Users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView
from Users.views import LogoutView, IndexView
from organization.views import OrgView
from MxOnline.settings import MEDIA_ROOT, STATIC_ROOT

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),

    url('^$', IndexView.as_view(), name="index"),
    # 这里调用的不是as_view这个句柄,所以要加上()
    url('^login/$', LoginView.as_view(), name="user_login"),
    url('^logout/$', LogoutView.as_view(), name="user_logout"),
    url('^register/$', RegisterView.as_view(), name="register"),

    # 验证码配置
    url(r'^captcha/', include('captcha.urls')),

    # 用户激活
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),

    # 找回密码
    url(r'^forget/$', ForgetPwdView.as_view(), name="forget_pwd"),

    # 重置密码链接
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name="reset_pwd"),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),

    # 课程机构URL配置
    url(r'^org/', include('organization.urls', namespace="org")),

    # 课程相关URL配置
    url(r'^course/', include('courses.urls', namespace="course")),

    # 处理media信息的URL
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # 在生产环境下处理静态文件
    url(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),

    # 用户中心配置
    url(r'^users/', include('Users.urls', namespace="users")),

]

# 全局404,500页面配置
handler404 = 'Users.views.page_not_found'
handler500 = 'Users.views.page_error'