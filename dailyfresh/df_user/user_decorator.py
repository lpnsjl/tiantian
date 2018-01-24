# -*- coding: UTF-8 -*-
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
def login(fun):
    def wrapper(request, *args, **kw):
        if 'user_id' in request.session:
            return fun(request, *args, **kw)
        else:
            red = HttpResponseRedirect('/user/login/')
            url = request.get_full_path()
            red.set_cookie('url', url)
            return red


    return wrapper
"""
装饰器，用于用户验证处理，用户未登录，转到登陆页，
并记录此次请求完整的url，便于登录成功后转向该页面；
如果已登陆过，直接转向要访问的页面

粗心大意不可取，return login_fun刚开始放错了位置，（多放进去了一个tab位）导致
TypeError: view must be a callable or a list/tuple in the case of include().
"""