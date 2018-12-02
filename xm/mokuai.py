import re

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from lxml import etree
import requests
import happybase as db

from xm.models import Info


class Project_require1:
    def __init__(self,data,page,city,position):
        self.data = data
        self.page = page
        self.city=city
        self.position=position
    def page1(self):
        # 生成Paginator对象 定义每一页50个数据
        paginator = Paginator(self.data,10)
        # 获取当前页码
        currentPage = int(self.page)
        try:
            print(self.page)
            data_list = paginator.page(self.page)  # 获取当前页码的记录
        except PageNotAnInteger:
            data_list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
        except EmptyPage:
            data_list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
        return [data_list, paginator, currentPage]
    def search(self):
        city=self.city
        position=self.position
        result = self.page1()
        data_list = result[0]
        paginator = result[1]
        currentPage = result[2]
        return locals()

class Project_require2:
    def __init__(self):
        pass
    #从hbase中获取数据
    def hbase(self,search_condition):
        conn = db.Connection(host='192.168.19.10', port=9090)
        conn.open()
        table = conn.table('pls_hbase:xm')
        data1=[]
        for key, value in table.scan(filter="RowFilter(=,'regexstring:\.*" + search_condition + ".*')"):
            data={}
            for i, v in value.items():
                if 'notshow' in i.decode('utf-8'):
                    pass
                else:
                    data.update({str(i.decode('utf-8')).split('show:')[1]: v.decode('utf-8')})
            data1.append(data)
        print(data1)
        return data1
    #将rz存入hbase  ip,search_time,userid,city,position,ip_city
    def hbase_rz(self,ip,search_time,userid,city,position,ip_city):
        conn = db.Connection(host='192.168.19.10', port=9090)
        conn.open()
        table = conn.table('pls_hbase:rz')
        #已ip_city作为rowkey 是为了之后查询往echarts中导数据更方便
        if userid is None:
            table.put(""+ip_city+"", {"data:用户ip":ip})
        else:
            table.put(""+ip_city + "", {"data:用户账号":userid})
        table.put("" +ip_city + "", {"data:用户查询时间":search_time})
        table.put("" +ip_city + "", {"data:用户查询职位":position})
        table.put("" +ip_city + "", {"data:用户查询职位所在城市":city})
        table.put("" +ip_city + "", {"data:用户所在城市":ip_city})
    #查询用户ip所在城市
    def checkip(self,ip):
        ip='219.143.103.233'
        url='http://www.ip138.com/ips1388.asp?ip='+ip+'&action=2'
        html=etree.HTML(requests.get(url).content.decode('gb2312'))
        data=str(html.xpath('//ul[@class="ul1"]/li/text()')[0])
        return data.split('本站数据：')[1]
    #从hbase中取出ip数据 在echarts中展示
    def get_rzData(self):
        conn = db.Connection(host='192.168.19.10', port=9090)
        conn.open()
        table = conn.table('pls_hbase:rz')
        t = table.scan()
        data = {}
        for k, v in list(t):
            if '北京' in k.decode('utf-8'):
                data.update({'beijing':len(v)})
            else:
                data.update({'beijing':0})
            if '天津' in k.decode('utf-8'):
                data.update({'tianjing':len(v)})
            else:
                data.update({'tianjing': 0})
            if '上海' in k.decode('utf-8'):
                data.update({'shanghai':len(v)})
            else:
                data.update({'shanghai': 0})
            if '重庆' in k.decode('utf-8'):
                data.update({'chongq': len(v)})
            else:
                data.update({'chongq': 0})
            if '河北' in k.decode('utf-8'):
                data.update({'heib': len(v)})
            else:
                data.update({'heib': 0})
            if '河南' in k.decode('utf-8'):
                data.update({'henan': len(v)})
            else:
                data.update({'henan': 0})
            if '云南' in k.decode('utf-8'):
                data.update({'yunnan': len(v)})
            else:
                data.update({'yunnan': 0})
            if '辽宁' in k.decode('utf-8'):
                data.update({'liaon': len(v)})
            else:
                data.update({'liaon': 0})
            if '黑龙江' in k.decode('utf-8'):
                data.update({'heilongj': len(v)})
            else:
                data.update({'heilongj': 0})
            if '湖南' in k.decode('utf-8'):
                data.update({'hunan': len(v)})
            else:
                data.update({'hunan': 0})
            if '安徽' in k.decode('utf-8'):
                data.update({'anh': len(v)})
            else:
                data.update({'anh': 0})
            if '山东' in k.decode('utf-8'):
                data.update({'shandong': len(v)})
            else:
                data.update({'shandong': 0})
            if '新疆' in k.decode('utf-8'):
                data.update({'xinjiang': len(v)})
            else:
                data.update({'xinjiang': 0})
            if '江苏' in k.decode('utf-8'):
                data.update({'jiangs': len(v)})
            else:
                data.update({'jiangs': 0})
            if '浙江' in k.decode('utf-8'):
                data.update({'zhejiang': len(v)})
            else:
                data.update({'zhejiang': 0})
            if '江西' in k.decode('utf-8'):
                data.update({'jiangx': len(v)})
            else:
                data.update({'jiangx': 0})
            if '湖北' in k.decode('utf-8'):
                data.update({'hubei': len(v)})
            else:
                data.update({'hubei': 0})
            if '广西' in k.decode('utf-8'):
                data.update({'guangx': len(v)})
            else:
                data.update({'guangx': 0})
            if '甘肃' in k.decode('utf-8'):
                data.update({'gansu': len(v)})
            else:
                data.update({'gansu': 0})
            if '山西' in k.decode('utf-8'):
                data.update({'shanx': len(v)})
            else:
                data.update({'shanx': 0})
            if '内蒙古' in k.decode('utf-8'):
                data.update({'neimenggu': len(v)})
            else:
                data.update({'neimenggu': 0})
            if '陕西' in k.decode('utf-8'):
                data.update({'shanx': len(v)})
            else:
                data.update({'shanx': 0})
            if '吉林' in k.decode('utf-8'):
                data.update({'jilin': len(v)})
            else:
                data.update({'jilin': 0})
            if '福建' in k.decode('utf-8'):
                data.update({'fujian': len(v)})
            else:
                data.update({'fujian': 0})
            if '贵州' in k.decode('utf-8'):
                data.update({'guiz': len(v)})
            else:
                data.update({'guiz': 0})
            if '广东' in k.decode('utf-8'):
                data.update({'guangd': len(v)})
            else:
                data.update({'guangd': 0})
            if '青海' in k.decode('utf-8'):
                data.update({'qinghai': len(v)})
            else:
                data.update({'qinghai': 0})
            if '西藏' in k.decode('utf-8'):
                data.update({'xizang': len(v)})
            else:
                data.update({'xizang': 0})
            if '四川' in k.decode('utf-8'):
                data.update({'sichuan': len(v)})
            else:
                data.update({'sichuan': 0})
            if '宁夏' in k.decode('utf-8'):
                data.update({'ningxia': len(v)})
            else:
                data.update({'ningxia': 0})
            if '海南' in k.decode('utf-8'):
                data.update({'hainan': len(v)})
            else:
                data.update({'hainan': 0})
            if '台湾' in k.decode('utf-8'):
                data.update({'taiw': len(v)})
            else:
                data.update({'taiw': 0})
            if '香港' in k.decode('utf-8'):
                data.update({'xianggang': len(v)})
            else:
                data.update({'xianggang': 0})
            if '澳门' in k.decode('utf-8'):
                data.update({'aom': len(v)})
            else:
                data.update({'aom': 0})
        return data

    #从mysql和hbase中获取数据 在echarts中展示
    def echarts_data(self,parm):
        # 从mysql中获取数据
        beijin = Info.objects.filter(city__icontains=parm[0])
        shanghai = Info.objects.filter(city__icontains=parm[1])
        guangzhou = Info.objects.filter(city__icontains=parm[2])
        shenzhen = Info.objects.filter(city__icontains=parm[3])
        # 从hbase中获取数据
        conn = db.Connection(host='192.168.19.10', port=9090)
        conn.open()
        table = conn.table('pls_hbase:xm')
        i = 0
        data2 = []
        while i < 4:
            data1 = []
            for key, value in table.scan(filter="RowFilter(=,'regexstring:\.*" + parm[i] + ".*')"):
                data = []
                for j,v in value.items():
                    data.append(v.decode('utf-8'))
                data1.append(data)
            result = len(data1)
            data2.append(result)
            i += 1
        return len(beijin) + data2[0], len(shanghai) + data2[1], len(guangzhou) + data2[2], len(shenzhen) + data2[3]


