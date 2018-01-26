# -*- coding: UTF-8 -*-
from django.conf.urls import url
from df_order import views


urlpatterns = [
    url(r'^$',views.order),
    url(r'^order_handle/$', views.order_handle),
]
