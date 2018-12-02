# from django.shortcuts import redirect
# from django.utils.deprecation import MiddlewareMixin
#
#
# class login_MiddleAware(MiddlewareMixin):
#     #如果验证成功，则什么一个不用做，否则返回HttpResponse即可响应请求(中断)
#     def process_request(self,request):#强制登录判断
#         if "login" not in request.path:
#             #路径中如果没有"login" 和 "register"  http://ip:port/xx/xxx/x
#             print("登录验证")
#             session = request.session #获取session
#             if session.get("login"): #判断是否有登录的标记
#                 print("已登录")
#             else:
#                 print("未登录")
#                 #return render(request,"login.html") #未登录则，跳转登录页面
#                 return redirect("/main/login/login_data/")
#         else:
#             print("正在登录") #如果路径中"login"则是登录动作本身
#     def process_response(self,request,response):
#         print("response:",request,response)
#         return response #持续返回响应