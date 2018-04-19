from django.contrib.auth.models import AbstractUser
from django.db import models

#使用Django自带的用户认证模块
from utils.models import BaseModel


class User(BaseModel,AbstractUser):
    """用户信息模型类"""

    class Meta(object):
        db_table = 'df_user'


class Address(BaseModel):
    """地址"""

    receiver_name = models.CharField(max_length=20, verbose_name="收件人")
    receiver_mobile = models.CharField(max_length=11, verbose_name="联系电话")
    detail_addr = models.CharField(max_length=256, verbose_name="详细地址")
    zip_code = models.CharField(max_length=6, null=True, verbose_name="邮政编码")
    #初始化非默认地址
    is_default = models.BooleanField(default=False, verbose_name='默认地址')
    #外键-地址对应用户
    user = models.ForeignKey(User, verbose_name="所属用户")

    class Meta:
        db_table = "df_address"
