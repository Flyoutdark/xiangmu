# Create your views here.
import random
import time
import re
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page

from xm.models import Regist,Info
from xm.mokuai import Project_require1,Project_require2
from django.core.cache import cache
def regist_page(request):
    return render(request,'register.html')
def regist_data(request):
    userid=request.POST.get('userid')
    usrtel=request.POST.get('usrtel')
    email=request.POST.get('email')
    psw=request.POST.get('psw')
    #存数据库
    Regist(userid=userid,usrtel=usrtel,email=email,psw=psw).save()
    return redirect('/main/login/login_page/')
def login_page(request):
    return render(request,'login.html')
def regist_user_ajax(request):
    data=request.GET.get('data')
    if Regist.objects.filter(userid=data) or len(data)==0:
        return HttpResponse('0')
    return HttpResponse('1')
def regist_tel_ajax(request):
    data=request.GET.get('data')
    myre = "^1\d{10}"
    res = re.findall(myre,data)
    if len(res)==len(data):
        return HttpResponse('1')
    return HttpResponse('0')
def regist_email_ajax(request):
    pass
def regist_pwd_ajax(request):
    data=request.GET.get('data')
    flag1=0
    flag2=0
    flag3=0
    for i in data:
        if i.isalnum():
            flag1=1
        if i.isdigit():
            flag2=1
        if i in r'~!@#$#$%^&&**())_+?><":"/.,;':
            flag3=1
    if len(data)>6 and flag1+flag2+flag3==3:
       return HttpResponse('1')
    return HttpResponse('0')
def login_data(request):
    userid=request.POST.get('userid')
    psw=request.POST.get('psw')
    #作判断
    if Regist.objects.filter(userid=userid,psw=psw):
        request.session['login']=userid
        if userid:
            t=userid+str(random.random()*10)
            request.session['userid'] =t
            return redirect('/main/detail_page/main_page/?userid=' + t)
        return redirect('/main/detail_page/main_page/')
    return redirect('/main/login/login_data/')

def main_page(request):
    userid=request.GET.get('userid')
    if userid:
        return render(request,"main.html",{'userid':userid})
    return render(request, "main.html")

#使用remote_addr抓取到的是127.0.0.1，所以使用Http_x_FORWARDED_FOR才获得的是用户的真实iP
#日志
def rz(fun):
    def zz(qwe):
        if qwe.META.get('HTTP_X_FORWARDED_FOR'):
            ip=qwe.META['HTTP_X_FORWARDED_FOR']
        else:
            ip=qwe.META['REMOTE_ADDR']
        #获取当前用户查询时间
        search_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        #获取用户查询的city 和position 和userid
        userid=qwe.GET.get('userid')
        city=qwe.GET.get('city')
        position=qwe.GET.get('position')
        #检验用户ip所在的城市 通过crawler模块获得
        search_ip=Project_require2()
        ip_city=search_ip.checkip(ip)
        #将ip search_time userid city position ip_city 存入hbase
        print('用户ip:'+str(ip),'用户查询时间：'+str(search_time),'用户账户:'+str(userid),'用户查询职位所在城市：'+str(city),'用户查询职位：'+str(position),'用户所在城市：'+str(ip_city))
        test=Project_require2()
        test.hbase_rz(ip,search_time,userid,city,position,ip_city)
        return fun(qwe)
    return zz
@rz
@cache_page(timeout=10)
def menu(request):
    """
        # 从mysql hbase中获取数据 便传递给模板
        # 从mysql获取
        # 从hbase获取
        # 分页
        :param request:
        :return:
    """
    #获取查询职位的城市
    city=request.GET.get('city')
    #获取查询职位
    position=request.GET.get('position')
    # 获取页码 默认是第一页
    page = request.GET.get('page',1)
    # 从数据库中获取所有数据 展示
    data = Info.objects.filter(position1__icontains=position,city=city)
    # page_data = Page(data,page,city,position)
    page_data=Project_require1(data,page,city,position)
    #设置标志 记数10页
    flag_noload=0
    #计访问次数 判别爬虫
    flag_crawler=0
    if request.session.get('userid'):
        #用户已经登录 正常访问 同时检测爬虫
        flag_crawler+=1
        time_start=time.time()
        if flag_crawler>=60:
            time_stop=time.time()
            if time_stop-time_start>60:
                flag_crawler=0
                return render(request, 'menu.html',page_data.search())
            else:
                return redirect('/main/detail_page/menu/?page=6')
        return render(request, 'menu.html', page_data.search())
    else:
        #用户未登录 只能查看前10页数据
        if int(page)>10:
            #大于10页则让登录
            # return redirect('/main/login/login_data/')
            return render(request,'redirect_login.html')
        return render(request, 'menu.html',page_data.search())
#按查询条件查询
@rz
def search_condition(request):
    # 根据search_condition作为查询条件，获取所有city相关的数据 data
    city=['北京','上海','广州','深圳']
    city=request.GET.get('city')
    position=request.GET.get('position')
    print(city,position)
    # 获取页码 默认是第一页
    page = request.GET.get('page', 1)
    if int(page) >= 10:
        if city!='':
            city=city
            position=''
            search_hbase=Project_require2()
            data=search_hbase.hbase(city)
        else:
            position=position
            city=''
            search_hbase = Project_require2()
            data = search_hbase.hbase(position)
    else:
        if city!='':
            city=city
            position=''
            data=Info.objects.filter(city=city)
        else:
            position=position
            city=''
            data=Info.objects.filter(position1__icontains=position)
    if request.session.get('userid'):
        # page_data = Page(data,page,city,position)
        page_data = Project_require1(data, page, city, position)
        return render(request,'menu_search.html',page_data.search())
    else:
        return redirect('/main/login/login_data/')

def intro(request):
    return render(request,'introduce.html')

def text(request):
    return render(request,'1.html')

#ip_chart
def ip_grap(request):
    #从hbase中取出rz数据
    result=Project_require2()
    data=result.get_rzData()
    return render(request,'地图.html',{'data':data})
#city_chart
def city_chart(request):
    parm = ['北京', '上海', '广州', '深圳']
    result = Project_require2()
    data=result.echarts_data(parm)
    return render(request,'柱状图.html',{'beijing':data[0],'shanghai':data[1],'guangzhou':data[2],'shenzhen':data[3]})

def position_chart(request):
    parm = ['AI', '爬虫', '大数据', 'python']
    result = Project_require2()
    data = result.echarts_data(parm)
    return render(request,'饼图.html',{'beijing':data[0],'shanghai':data[1],'guangzhou':data[2],'shenzhen':data[3]})