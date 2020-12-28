import datetime

from django.shortcuts import render, redirect, get_object_or_404

from business.models import Business
from customer.models import Customer
from liaison.models import Liaison
from record.models import Record
from users import forms
from users.models import User, Count


def index(request):
    """页面登录根据用户是否登录进行重定向"""
    if not request.session.get('is_login', None):
        return redirect('login')
    else:
        return redirect('home')


def home(request):
    """系统首页"""

    # 初始化用户的统计数据
    user_id = request.session.get('user_id')
    user_name = request.session.get('user_name')
    Count.objects.get_or_create(user_id=user_id, name=user_name)

    # 获取月份和当天日期
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    print(month, day)

    # 统计数量
    customer = Customer.objects.filter(user=user_id)
    liaison = Liaison.objects.filter(user=user_id)
    record = Record.objects.filter(user=user_id)
    business = Business.objects.filter(user=user_id)

    month_customer = customer.filter(created_at__year=year, created_at__month=month).count()  # 每月统计
    month_liaison = liaison.filter(created_at__year=year, created_at__month=month).count()  # 每月统计
    month_record = record.filter(created_at__year=year, created_at__month=month).count()  # 每月统计
    month_business = business.filter(created_at__year=year, created_at__month=month).count()  # 每月统计

    day_customer = customer.filter(created_at__year=year, created_at__month=month, created_at__day=day).count()  # 每天统计
    day_liaison = liaison.filter(created_at__year=year, created_at__month=month, created_at__day=day).count()  # 每天统计
    day_record = record.filter(created_at__year=year, created_at__month=month, created_at__day=day).count()  # 每天统计
    day_business = business.filter(created_at__year=year, created_at__month=month, created_at__day=day).count()  # 每天统计

    all_customer = customer.filter().count()  # 全部
    all_liaison = liaison.filter().count()  # 全部
    all_record = record.filter().count()  # 全部
    all_business = business.filter().count()  # 全部

    Count.objects.filter(user_id=user_id).update(day_customer=day_customer, day_liaison=day_liaison,
                                                 day_record=day_record, day_business=day_business,
                                                 month_customer=month_customer, month_liaison=month_liaison,
                                                 month_record=month_record, month_business=month_business,
                                                 all_customer=all_customer, all_liaison=all_liaison,
                                                 all_record=all_record, all_business=all_business)

    # 渲染数据到home页面
    counts = Count.objects.all()
    return render(request, 'home.html', {
        'counts': counts
    })


def login(request):
    """系统登录"""
    if request.session.get('is_login', None):
        return redirect('index')
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '请输入账号和密码！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username', None)
            password = login_form.cleaned_data.get('password', None)
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
