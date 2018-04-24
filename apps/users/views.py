import re

from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django_redis import get_redis_connection
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired

from apps.goods.models import GoodsSKU
from celery_task.tasks import send_active_email
from Mystore import settings
from apps.users.models import User, Address
from utils.common import LoginRequireView


def register(request):
    return render(request, 'register.html')


def do_register(request):
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


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
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
            # django内置函数，自动创建用户
            user = User.objects.create_user(username=username, email=email,
                                            password=password)  # type: User
            user.is_active = False
            # 存储用户
            user.save()
            # 命名重复发生异常
        except IntegrityError:
            return render(request, 'register.html', {'message': '用户已经存在'})

        # 发送激活邮件
        # user_id加密后的结果称之为 token(口令、令牌)
        token = user.active_token()

        # send_active_email(username,email,token)
        # 使用celery异步发送激活邮件
        send_active_email.delay(username, email, token)
        # 响应请求
        return HttpResponse('注册成功')


class ActiveView(View):
    def get(self, request, token: str):
        # 得到用户id
        try:
            s = TimedJSONWebSignatureSerializer(settings.SECRET_KEY)
            print(token)
            info = s.loads(token)
            user_id = info['confirm']
        except SignatureExpired:
            return HttpResponse('链接已经过期')

        User.objects.filter(id=user_id).update(is_active=True)
        return HttpResponse('激活成功，进入登陆页面')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        remeber = request.POST.get('remeber')
        #合法性
        if not all([username,password]):
            return render(request,'login.html',{'message':'Empty'})

        user = authenticate(username=username,password=password) # type:User

        if user is None:
            return render(request, 'login.html', {'message': 'error'})
        if not user.is_active:
            return render(request, 'login.html', {'message': '未激活'})
        #保存登陆状态，session封装用户的信息
        #request.session()
        login(request,user)
        # 记住用户功能就是设置session有效期
        if remeber == 'on':
            request.session.set_expiry(None)
        else:
            request.session.set_expiry(0)
        # return redirect(reverse('goods:index'))
        #next参数操作
        next = request.GET.get('next')
        if next:
            return redirect(next)
        else:
            return redirect(reverse('goods:index'))


class LogoutView(View):
    def get(self,request):
        '''清除session数据'''
        logout(request)
        return redirect(reverse('goods:index'))


class UserAddressView(LoginRequireView,View):
    def get(self, request):
        #显示用户的收货地址
        user = request.user
        try:
            address = user.address_set.latest('create_time')
        except Address.DoesNotExist:
            address = None
        context = {
            'which_page':1,
            'address':address
        }
        return render(request, 'user_center_site.html')
    def post(self,request):
        receiver = request.POST.get('receiver')
        address = request.POST.get('address')
        zip_code = request.POST.get('zip_code')
        mobile = request.POST.get('mobile')
        if not all([receiver, address, mobile]):
            return render(request, 'user_center_site.html', {'errmsg': '参数不完整'})

        #新增地址
        #登陆后用户保存在request
        Address.objects.create(
            receiver_name=receiver,
            receiver_mobile=mobile,
            detail_addr=address,
            zip_code=zip_code,
            user=request.user
        )
        return redirect(reverse('user:address'))


class UserOrderView(LoginRequireView,View):
    def get(self, request):
        context = {
            'which_page': 2
        }
        return render(request, 'user_center_order.html')


class UserInfoView(LoginRequireView,View):
    def get(self, request):
        # todo 从redis读取浏览记录
        strict_redis = get_redis_connection()  #type: StrictRedis
        key = 'history_%s'%request.user.id
        sku_ids = strict_redis.lrange(key,0,4)

        skus = []
        for sku in sku_ids:
            s = GoodsSKU.objects.get(id = sku)
            skus.append(s)


        context = {
            'which_page': 3,
            'skus':skus,
        }
        return render(request, 'user_center_info.html',context)
