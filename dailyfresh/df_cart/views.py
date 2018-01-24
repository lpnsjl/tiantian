from django.shortcuts import render
from df_cart.models import *
from df_user import user_decorator
from django.http import JsonResponse


@user_decorator.login
def cart(request):
    uid = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=uid)
    # print (carts[2].goods.gname)
    context = {
        'carts': carts,

    }
    return render(request, 'df_cart/cart.html',context)

@user_decorator.login
def add(request, gid, count):
    uid = request.session['user_id']
    gid = int(gid)
    count = int(count)
    carts = CartInfo.objects.filter(user_id=uid, goods_id=gid)
    # 用户已购买过商品
    if len(carts)>=1:
        cart1 = carts[0]
        cart1.cnumber =cart1.cnumber + count
    # 用户未购买过该商品
    else:
        cart1 = CartInfo()
        cart1.user_id = uid
        cart1.goods_id = gid
        cart1.cnumber = count
    # 将该用户购买情况加入购物车表
    cart1.save()
    count = CartInfo.objects.filter(user_id=uid,goods_id=gid)[0].cnumber
    return JsonResponse({'count':count,'cart_id':cart1.id})
@user_decorator.login
def edit(request, cid, count):
    uid = request.session['user_id']
    cart1 = CartInfo.objects.get(pk=int(cid))# cid购物车id
    cart1.cnumber = int(count)
    cart1.save()
    return JsonResponse({'data':int(count)})
@user_decorator.login
def delete(request, cid):
    cart1 = CartInfo.objects.get(pk=int(cid))
    cart1.delete()
    return JsonResponse({'data':0})
