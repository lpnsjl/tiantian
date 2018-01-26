from django.db import models


class OrderInfo(models.Model):
    # 订单号
    oid = models.CharField(max_length=20)
    odate = models.DateTimeField(auto_now=True)
    oIspay = models.BooleanField(default=False)
    ototal = models.DecimalField(max_digits=8, decimal_places=2)
    oaddress = models.CharField(max_length=100)
    user = models.ForeignKey('df_user.UserInfo', on_delete=models.CASCADE)

# 订单详细信息
class OrderDetailInfo(models.Model):
    goods = models.ForeignKey('df_goods.GoodsInfo', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    order = models.ForeignKey('OrderInfo', on_delete=models.CASCADE)
    count = models.IntegerField()
