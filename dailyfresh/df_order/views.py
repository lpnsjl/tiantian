from django.shortcuts import render,redirect
from df_user import user_decorator
from df_cart.models import *
from df_user.models import *
from django.db import transaction
from df_order.models import *
from datetime import datetime


@user_decorator.login
def order(request):
    user_id = request.session['user_id']
    user = UserInfo.objects.get(id=user_id)
    get = request.GET
    # 得到购物车表中所购买物品的id号
    cart_ids = get.getlist('cart_id')
    cart_ids1 = [int(cart_id) for cart_id in cart_ids]
    carts = CartInfo.objects.filter(id__in=cart_ids1)
    # print (carts[0].goods.gpic)
    count = len(carts)
    context = {
        'carts': carts,
        'user': user,
        'count': count,
        'cart_ids': ','.join(cart_ids),

    }
    return render(request, 'df_order/place_order.html',context)


@transaction.atomic()
@user_decorator.login
def order_handle(request):
    tran_id = transaction.savepoint()
    uid = request.session['user_id']
    print(uid)
    user = UserInfo.objects.get(id=uid)
    post = request.POST
    # 订单信息
    try:
        order = OrderInfo()
        now = datetime.now()
        order.oid = '%s%d'%(now.strftime('%Y%m%d%H%M%S'), uid)
        order.date = now
        order.ototal = post['total_1']
        order.user_id = uid
        order.oaddress = post['address']
        order.save()
        cart_ids = post['cart_ids']
        cart_ids1 = [int(item) for item in cart_ids.split(',')]
        # print (cart_ids1)
        carts = CartInfo.objects.filter(id__in=cart_ids1)
        # print (carts)
        # 订单详情
        for cart in carts:
            goods = cart.goods
            # 库存足够
            if goods.gkucun > cart.cnumber:
                goods.gkucun = goods.gkucun - cart.cnumber
                goods.save()
                orderdetail = OrderDetailInfo()
                orderdetail.goods_id = goods.id
                orderdetail.price = goods.gprice
                # print (orderdetail.price)
                orderdetail.order_id = order.id
                orderdetail.count = cart.cnumber
                orderdetail.save()
                cart.delete()
            else:
                transaction.savepoint_rollback(tran_id)
                return redirect('/cart/')
        transaction.savepoint_commit(tran_id)
    except:
        transaction.savepoint_rollback(tran_id)

    return redirect('/user/order/')


