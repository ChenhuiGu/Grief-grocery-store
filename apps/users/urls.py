from django.conf.urls import include, url
from django.contrib import admin

from apps.users import views

urlpatterns = [
    # url(r'^register$',views.register),
    # url(r'^do_register$',views.do_register)
    #类视图同时处理get和post请求
    url(r'^register$',views.RegisterView.as_view(),name='register'),
    url(r'^active/(.+)$',views.ActiveView.as_view(),name='active'),
    url(r'^login$',views.LoginView.as_view(),name='login'),
    url(r'^logout$',views.LogoutView.as_view(),name='logout'),
    url(r'^address$', views.UserAddressView.as_view(), name='address'),  # 用户中心:地址
    url(r'^orders$', views.UserOrderView.as_view(), name='orders'),  # 用户中心:订单
    url(r'^$', views.UserInfoView.as_view(), name='info'),  # 用户中心:个人信息
]
