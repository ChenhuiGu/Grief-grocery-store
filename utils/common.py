from django.contrib.auth.decorators import login_required

#mro 多继承的顺序
# from django.http import request
from django.views.generic import View

from django_redis import get_redis_connection
from redis import StrictRedis


class LoginRequireView(object):
    @classmethod
    def as_view(cls, **initkwargs):
        # 调用父类view的as_view方法, 并返回视图函数
        view_fun = super().as_view(**initkwargs)
        # 对视图函数进行装饰
        # 返回装饰后的视图函数
        return login_required(view_fun)


class CartCountView(View):
    '''购物车数量显示'''
    # 已登录，未登陆
    # cookie或redis
    def get_cart_count(self,request):
        cart_count = 0
        if request.user.is_authenticated():
            strict_redis = get_redis_connection() # type: StrictRedis
            key = 'cart_%s'%request.user.id
            # print(key)
            cart_dict = strict_redis.hvals(key)
            # print(cart_dict)  [b'2', b'3', b'2']
            # 返回 list类型，存储的元素是 bytes,转为整形进行运算
            for count in cart_dict:
                cart_count += int(count)
        return cart_count

