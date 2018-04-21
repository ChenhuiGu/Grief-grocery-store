import re
from django.db.utils import IntegrityError
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired
from celery_task.tasks import send_active_email
from Mystore import settings
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
            #django内置函数，自动创建用户
            user = User.objects.create_user(username=username, email=email,
                                            password=password)  # type: User
            user.is_active = False
            #存储用户
            user.save()
            #命名重复发生异常
        except IntegrityError:
            return render(request, 'register.html', {'message': '用户已经存在'})

        #发送激活邮件
        #user_id加密后的结果称之为 token(口令、令牌)
        token = user.active_token()

        # send_active_email(username,email,token)
        #使用celery异步发送激活邮件
        send_active_email.delay(username,email,token)
        # 响应请求
        return HttpResponse('注册成功')


class ActiveView(View):
    def get(self,request,token:str):
        #得到用户id
        try:
            s = TimedJSONWebSignatureSerializer(settings.SECRET_KEY)
            print(token)
            info = s.loads(token)
            user_id = info['confirm']
        except SignatureExpired:
            return HttpResponse('链接已经过期')

        User.objects.filter(id=user_id).update(is_active=True)
        return HttpResponse('激活成功，进入登陆页面')



