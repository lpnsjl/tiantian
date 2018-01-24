
from django.shortcuts import render,redirect
from df_user.models import *
from hashlib import sha1
from django.http import JsonResponse,HttpResponseRedirect
from df_user import user_decorator
from df_goods.models import *


# 用户注册页面
def register(request):
    context = {'title': '注册'}
    return render(request, 'df_user/register.html',context)

# 用户注册处理
def register_handle(request):
    # 接收用户注册信息
    post = request.POST
    user = UserInfo()
    user.uname = post['user_name']
    user.upwd = post['pwd']
    cpwd = post['cpwd']
    user.uemail = post['email']
    # 判断两次密码
    if cpwd != user.upwd or user.uname == '' or user.upwd == '' or user.uemail == '':
        return redirect('/user/register')

    # 密码加密
    s1 = sha1()
    s1.update(user.upwd.encode('utf-8'))
    user.upwd = s1.hexdigest()

    # 用户信息提交数据库
    user.save()
    # 创建成功转到登录页面
    return redirect('/user/login')

# 检查用户名是否存在
def register_exist(request):
    uname = request.GET.get('uname')
    # 用户名被注册，count=1
    count = UserInfo.objects.filter(uname=uname).count()
    print (count)
    return JsonResponse({'count':count})


# 登录页面
def login(request):
    uname = request.COOKIES.get('uname','')
    context = {'title': '登录', 'error_name': 0, 'error_pwd': 0,'uname': uname}
    return render(request, 'df_user/login.html',context)

# 登录处理
def login_handle(request):
    # 提取用户登录信息
    post = request.POST
    uname = post['username']
    upwd = post['pwd']
    jizhu = post.get('jizhu', 0)

    # 判断用户是否存在
    user = UserInfo.objects.filter(uname=uname)# 返回一个查询结果的数组
    if len(user) == 1:
        # 密码加密
        s1 = sha1()
        s1.update(upwd.encode('utf-8'))
        if s1.hexdigest() == user[0].upwd:
            url = request.COOKIES.get('url', '/index')
            red = HttpResponseRedirect(url)
            # 成功转向后，删除地址，防止以后直接登录造成的转向
            red.set_cookie('url', '', max_age=-1)
            if jizhu == 1:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)
            request.session['user_id'] = user[0].id
            request.session['uname'] = user[0].uname
            return red

        else:
            context = {'title': '登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname, 'upwd': upwd}
            return render(request, 'df_user/login.html', context)
    else:
        context = {'title': '登录', 'error_name': 1, 'error_pwd': 0,'uname': uname,'upwd':upwd}
        return render(request,'df_user/login.html',context)
# 用户退出
def logout(request):
    request.session.flush()
    return redirect('/index')

# 用户中心个人信息页面
@user_decorator.login
def user_center_info(request):
    uemail = UserInfo.objects.filter(id=request.session['user_id'])[0].uemail
    # 最近浏览的商品
    goods_ids = request.COOKIES.get('goods_ids', '')
    if goods_ids == '':
        context = {'uname': request.session['uname'],
                   'uemail': uemail,
                   'goods_ids': goods_ids,
                   }
    else:
        print (goods_ids)
        zuijin = goods_ids.split(',')
        goods_list = []
        for id in zuijin:
            goods_list.append(GoodsInfo.objects.filter(id=int(id))[0])

        # print (goods_list[0])

        context = {'uname': request.session['uname'],
               'uemail': uemail,
               'goods_list': goods_list,
               'goods_ids': goods_ids,
               }
    return render(request, 'df_user/user_center_info.html', context)

# 用户个人订单信息
@user_decorator.login
def user_center_order(request):
    return render(request, 'df_user/user_center_order.html')

# 用户地址信息
@user_decorator.login
def user_center_site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uyoubian = post.get('uyoubian')
        user.uphone = post.get('uphone')
        user.save()
    context = {'title': '用户中心', 'user': user,
               'page_name': 1}
    return render(request, 'df_user/user_center_site.html', context)

