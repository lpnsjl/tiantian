from django.contrib import admin
from df_goods.models import *


class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'tname']
    list_filter = ['tname']
    search_fields = ['tname']

class GoodsInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'gname', 'gpic', 'gprice', 'gclick', 'gkucun']
    list_filter = ['gname']
    search_fields = ['gname']
    list_per_page = 6

admin.site.register(TypeInfo, TypeInfoAdmin)
admin.site.register(GoodsInfo, GoodsInfoAdmin)
