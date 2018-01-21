from django.db import models
from tinymce.models import HTMLField


class TypeInfo(models.Model):
    tname = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.tname

class GoodsInfo(models.Model):
    gname = models.CharField(max_length=20)
    # 商品图片，最终将传到页面，等同于向页面上传图片
    gpic = models.ImageField(upload_to='')
    gprice = models.DecimalField(max_digits=5, decimal_places=2)
    gunit = models.CharField(max_length=20, default='500g')
    isDelete = models.BooleanField(default=False)
    # 商品点击量，代表人气
    gclick = models.IntegerField()
    gjianjie = models.CharField(max_length=200)
    # 便于后台管理
    gcontent = HTMLField()
    # 库存
    gkucun = models.IntegerField()
    # 商品推荐，默认不推荐
    gtuijian = models.BooleanField(default=False)
    gtype = models.ForeignKey('TypeInfo', on_delete=models.CASCADE)

    def __str__(self):
        return self.gname
