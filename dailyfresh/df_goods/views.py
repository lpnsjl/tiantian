from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator


# 首页视图
def index(request):
    typelist = TypeInfo.objects.filter(isDelete=False)
    # 选出最新的四条数据和最热的四条数据
    type0 = typelist[0].goodsinfo_set.all().order_by('-id')[0:4]
    type01 = typelist[0].goodsinfo_set.all().order_by('-gclick')[0:4]
    type1 = typelist[1].goodsinfo_set.all().order_by('-id')[0:4]
    type11 = typelist[1].goodsinfo_set.all().order_by('-gclick')[0:4]
    type2 = typelist[2].goodsinfo_set.all().order_by('-id')[0:4]
    type21 = typelist[2].goodsinfo_set.all().order_by('-gclick')[0:4]
    type3 = typelist[3].goodsinfo_set.all().order_by('-id')[0:4]
    type31 = typelist[3].goodsinfo_set.all().order_by('-gclick')[0:4]
    type4 = typelist[4].goodsinfo_set.all().order_by('-id')[0:4]
    type41 = typelist[4].goodsinfo_set.all().order_by('-gclick')[0:4]
    type5 = typelist[5].goodsinfo_set.all().order_by('-id')[0:4]
    type51 = typelist[5].goodsinfo_set.all().order_by('-gclick')[0:4]

    context ={
        'type0': type0, 'type01': type01,
        'type1': type1, 'type11': type11,
        'type2': type2, 'type21': type21,
        'type3': type3, 'type31': type31,
        'type4': type4, 'type41': type41,
        'type5': type5, 'type51': type01,
    }

    return render(request, 'df_goods/index.html',context)

# 详情页视图
def detail(request, id):
    return render(request, 'df_goods/detail.html')

# 列表页视图
def list(request,tid,pindex,sort):
    # 得到商品种类对象
    typeinfo = TypeInfo.objects.get(id=int(tid))
    # 该种类的最新的两种商品
    news = typeinfo.goodsinfo_set.all().order_by('-id')[0:2]
    if sort == '1':
        # 默认排序，最新
        goods_list = typeinfo.goodsinfo_set.all().order_by('-id')
    if sort == '2':
        # 价格排序
        goods_list = typeinfo.goodsinfo_set.all().order_by('-gprice')
    if sort == '3':
        # 人气排序，点击量
        goods_list = typeinfo.goodsinfo_set.all().order_by('-gclick')

    paginator = Paginator(goods_list, 3)
    p = paginator.page(int(pindex))
    context = {
        'typeinfo': typeinfo,
        'news': news,
        'page': p,
        'goods_list': p.object_list,
        'paginator': paginator,
        'sort': sort,

    }
    return render(request, 'df_goods/list.html', context)