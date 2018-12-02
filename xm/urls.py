from django.contrib import admin
from django.urls import path, include

from xm import views

urlpatterns = [
path('regist/',include((
    [
        path('regist_page/',views.regist_page,name="regist_page"),
        path('regist_data/',views.regist_data,name="regist_data"),
        path('regist_user_ajax/',views.regist_user_ajax,name="regist_user_ajax"),
        path('regist_tel_ajax/',views.regist_tel_ajax,name="regist_tel_ajax"),
        path('regist_email_ajax/',views.regist_email_ajax,name="regist_email_ajax"),
        path('regist_pwd_ajax/',views.regist_pwd_ajax,name="regist_pwd_ajax"),
    ]))),
path('login/',include(([
        path('login_page/',views.login_page,name='login_page'),
        path('login_data/',views.login_data,name='login_data')
                        ]))),
path('detail_page/',include((
    [
        path('main_page/',views.main_page,name="main_page"),
        path('intro/',views.intro,name="intro"),
        path('menu/',views.menu,name="menu")
    ]))),
path('search/',include((
    [
        path('search_condition/',views.search_condition,name='search_condition'),
    ]))),
path('echarts/',include((
    [
        path('ip_grap/', views.ip_grap,name='ip_grap'),
        path('position_chart/',views.position_chart,name='position_chart'),
        path('city_chart/',views.city_chart,name='city_chart')
    ])))
]