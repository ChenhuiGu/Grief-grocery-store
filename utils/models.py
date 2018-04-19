
from django.db import models

class BaseModel(models.Model):
    #基类
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')

    # python包未定义
    class Meta(object):
        abstract = True