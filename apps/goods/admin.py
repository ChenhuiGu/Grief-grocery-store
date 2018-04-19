from django.contrib import admin

from apps.goods.models import *

admin.site.register([GoodsCategory,GoodsSPU,GoodsSKU,GoodsImage,
                     IndexSlideGoods,IndexCategoryGoods,IndexPromotion,])
