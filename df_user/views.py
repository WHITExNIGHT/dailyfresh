from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from .models import *
from hashlib import sha1


def register(request):
    return render(request, 'df_user/register.html', {'title': '注册'})


def register_handle(request):
    # 接收用户输入
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')

    if len(uname) < 8:
        return redirect('/user/register/')
    count = UserInfo.objects.filter(uname=uname).count()
    if count > 0:
        # return render(request, '/user/register/', {'count': count})
        # return redirect('/user/register/')
        return render(request, 'df_user/register.html', {'error': 1})
    if upwd == '':
        return redirect('/user/register/')
    if uemail == '':
        return redirect('/user/register/')
    # 判断密码
    if upwd != upwd2:
        return redirect('/user/register/')
    # 密码加密
    s1 = sha1()
    s1.update(upwd.encode("utf-8"))  # 指定编码格式，否则会报错
    upwd3 = s1.hexdigest()
    # 创建对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()
    # 注册成功，转到登录页面
    return redirect('/user/login/')


# 不起作用
def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count': count})


def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 0, 'uname': uname}
    return render(request, 'df_user/login.html', context)


def login_handle(request):
    # 接收请求信息
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu', 0)
    # 根据用户登录查询对象
    users = UserInfo.objects.filter(uname=uname)  # []
    print(uname)
    # 判段用户名是否准确，准确则继续判断密码
    if len(users) == 1:
        s1 = sha1()
        s1.update(upwd.encode("utf-8"))
        if s1.hexdigest() == users[0].upwd:
            red = HttpResponseRedirect('/user/info/')
            # 记住用户名
            if jizhu != 0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            return red
        else:
            context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname, 'upwd': upwd}
            return render(request, 'df_user/login.html', context)
    else:
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname, 'upwd': upwd}
        return render(request, 'df_user/login.html', context)


def info(request):
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail
    context = {
        'title': '用户中心',
        'user_email': user_email,
        'user_name': request.session['user_name'],
        'page_name': 1
    }
    return render(request, 'df_user/user_center_info.html', context)


def order(request):
    context = {'title': '用户中心',
               'user_name': request.session['user_name'],
               'page_name': 1}
    return render(request, 'df_user/user_center_order.html', context)


def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        user.ushou = post.get('ushow')
        user.uaddress = post.get('uaddress')
        user.uyoubian = post.get('uyoubian')
        user.uphone = post.get('uphone')
        user.save()
    context = {'title': '用户中心', 'user': user,
               'user_name': request.session['user_name'],
               'page_name': 1}
    return render(request, 'df_user/user_center_site.html', context)
