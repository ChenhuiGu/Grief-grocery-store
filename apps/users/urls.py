from django.conf.urls import include, url
from django.contrib import admin

from apps.users import views

urlpatterns = [
    # url(r'^register$',views.register),
    # url(r'^do_register$',views.do_register)
    #类视图同时处理get和post请求
    url(r'^register$',views.RegisterView.as_view(),name='register')
]
