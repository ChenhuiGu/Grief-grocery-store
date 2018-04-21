import re
from django.db.utils import IntegrityError
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from apps.users.models import User


def register(request):
    return render(request,'register.html')


def do_register(request):
    # 获取post请求,修改html
    username = request.POST.get('username')
    password = request.POST.get('password')
    password2 = request.POST.get('password2')
    email = request.POST.get('email')
    allow = request.POST.get('allow')  #如果被勾选，post传值为on
    #检验参数合法性
        # all函数   参数不为空
    if not all([username, password, password2, email]):
        return render(request,'register.html',{'message':'参数不能为空'})
        #规则
        #密码一致,合法性
    if not password == password2:
        return render(request, 'register.html', {'message': '密码不一致'})
        #邮箱合法
    if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
        return render(request, 'register.html', {'message': '邮箱格式不正确'})
        #勾选用户协议
    if allow != 'on':
        return render(request, 'register.html', {'message': '请勾选用户协议'})

    #保存用户信息到数据库
        #django自带保存信息
        #修改激活状态
        #判断用户是否存在
    user = None
    try:
        user = User.objects.create_user(username=username,email=email,
                                 password=password)
        user.is_active = False
    except IntegrityError:
        return render(request,'register.html',{'message':'用户已经存在'})


    #todo 发送激活邮件

    #响应请求
    return HttpResponse('注册成功')

class RegisterView(View):
    def get(self,request):
        return render(request, 'register.html')
    def post(self,request):
        # 获取post请求,修改html
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        allow = request.POST.get('allow')  # 如果被勾选，post传值为on
        # 检验参数合法性
        # all函数   参数不为空
        if not all([username, password, password2, email]):
            return render(request, 'register.html', {'message': '参数不能为空'})
            # 规则
            # 密码一致,合法性
        if not password == password2:
            return render(request, 'register.html', {'message': '密码不一致'})
            # 邮箱合法
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'message': '邮箱格式不正确'})
            # 勾选用户协议
        if allow != 'on':
            return render(request, 'register.html', {'message': '请勾选用户协议'})

            # 保存用户信息到数据库
            # django自带保存信息
            # 修改激活状态
            # 判断用户是否存在
        user = None
        try:
            user = User.objects.create_user(username=username, email=email,
                                            password=password)
            user.is_active = False
        except IntegrityError:
            return render(request, 'register.html', {'message': '用户已经存在'})

        # todo 发送激活邮件

        # 响应请求
        return HttpResponse('注册成功')
