from django.shortcuts import render
from django.views.generic import View

from apps.goods.models import GoodsCategory, IndexCategoryGoods, IndexSlideGoods, IndexPromotion
from utils.common import CartCountView


class IndexView(CartCountView):
    def get2(self,request):
        #显示用户名

        # user_id = request.session.get()
        # return render(request, 'index.html')

        # 自带
        # user = request.user
        return render(request,'index.html')

    def get(self,request):
        # 查询首页商品数据：商品类别，轮播图， 促销活动
        # 排序，抽取部分展示
        categories = GoodsCategory.objects.all()
        slide_skus = IndexSlideGoods.objects.all().order_by('index')
        promotions = IndexPromotion.objects.all().order_by('index')


        #展示首页商品
        for c in categories:
            text_skus = IndexCategoryGoods.objects.filter(display_type=0,category=c).order_by('index')
            image_skus = IndexCategoryGoods.objects.filter(display_type=1,category=c).order_by('index')[0:4]
            c.text_skus = text_skus
            c.image_skus = image_skus

        cart_count = super().get_cart_count(request)

        context = {
            'categories':categories,
            'slide_skus':slide_skus,
            'promotions':promotions,
            'cart_count':cart_count
        }
        return render(request,'index.html',context)