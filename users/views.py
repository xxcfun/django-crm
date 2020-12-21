from django.shortcuts import render, redirect, get_object_or_404

from users import forms
from users.models import User


def index(request):
    """页面登录根据用户是否登录进行重定向"""
    if not request.session.get('is_login', None):
        return redirect('login')
    else:
        return redirect('home')


def home(request):
    """系统首页"""
    pass
    return render(request, 'home.html', {

    })


def login(request):
    """系统登录"""
    if request.session.get('is_login', None):
        return redirect('index')
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '请输入账号和密码！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            try:
                user = User.objects.get(name=username)
            except:
                message = '用户不存在！'
                return render(request, 'login.html', locals())
            if user.password == password:
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                request.session['user_role'] = user.role
                return redirect('index')
            else:
                message = '密码不正确'
                return render(request, 'login.html', locals())
        else:
            return render(request, 'login.html', locals())
    login_form = forms.UserForm()
    return render(request, 'login.html', locals())


def mine(request):
    """个人中心模块"""
    pk = request.session.get('user_id')
    user = get_object_or_404(User, pk=pk, is_valid=True)
    if request.method == 'POST':
        editpwd = request.POST.get('editpwd')
        checkpwd = request.POST.get('checkpwd')
        if editpwd != checkpwd:
            message = '两次密码不一致'
        else:
            User.objects.filter(pk=pk).update(password=checkpwd)
            message = '修改成功'
    return render(request, 'mine.html', locals())


def logout(request):
    """退出登录"""
    if not request.session.get('is_login', None):
        return redirect('login')
    request.session.flush()
    return redirect('login')
