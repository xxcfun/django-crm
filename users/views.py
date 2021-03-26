import datetime

from django.shortcuts import render, redirect, get_object_or_404

from business.models import Business
from customer.models import Customer
from liaison.models import Liaison
from record.models import Record
from users import forms
from users.models import User, Count, Date
from utils import constants


def index(request):
    """页面登录根据用户是否登录进行重定向"""
    if not request.session.get('is_login', None):
        return redirect('login')
    else:
        return redirect('home')


def home(request):
    """系统首页"""
    if not request.session.get('is_login',  None):
        return redirect('login')
    # 初始化用户的统计数据
    user_id = request.session.get('user_id')
    user_name = request.session.get('user_name')
    Count.objects.get_or_create(user_id=user_id, name=user_name)

    # 获取月份和当天日期
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day

    now = datetime.datetime.now()
    yesterday = now - datetime.timedelta(days=1)
    yesterday_year = yesterday.year
    yesterday_month = yesterday.month
    yesterday_day = yesterday.day

    day_num = now.isoweekday()
    week_day = now - datetime.timedelta(days=day_num)

    # 统计数量
    counts = Count.objects.all()
    for count in counts:
        customer = Customer.objects.filter(user=count.user_id)
        record = Record.objects.filter(user=count.user_id)
        business = Business.objects.filter(user=count.user_id)

        # 昨日拜访
        yesterday_record = record.filter(status=constants.STATUS_XX,
                                         created_at__year=yesterday_year, created_at__month=yesterday_month,
                                         created_at__day=yesterday_day).count()
        # 昨日外呼
        yesterday_phone = record.filter(status=constants.STATUS_XS,
                                         created_at__year=yesterday_year, created_at__month=yesterday_month,
                                         created_at__day=yesterday_day).count()
        # 新增客户
        new_customer = customer.filter(created_at__year=year, created_at__month=month, created_at__day=day).count()
        # 新增商机
        new_business = business.filter(created_at__year=year, created_at__month=month, created_at__day=day).count()

        # 本周拜访
        week_record = record.filter(created_at__range=(week_day, now), status=constants.STATUS_XX).count()
        # 本周外呼
        week_phone = record.filter(created_at__range=(week_day, now), status=constants.STATUS_XS).count()
        # 本周商机
        week_business = business.filter(created_at__range=(week_day, now)).count()

        # # 控创
        # # 全部客户
        # all_customer = customer.filter().count()
        month_customer = customer.filter(created_at__year=year, created_at__month=month).count()
        # 跟进商机
        follow_business = business.exclude(winning_rate=constants.WINNING_DONE).count()
        # 完成商机
        finish_business = business.filter(winning_rate=constants.WINNING_DONE).count()

        # 更新数据
        Count.objects.filter(user_id=count.user_id).update(
            yesterday_record=yesterday_record, yesterday_phone=yesterday_phone,
            new_customer=new_customer, new_business=new_business,
            week_record=week_record, week_phone=week_phone, week_business=week_business,
            month_customer=month_customer, follow_business=follow_business, finish_business=finish_business
        )

    # 渲染数据到home页面
    counts = Count.objects.exclude(user_id=1)
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


def week(request):
    """周数据汇总"""
    if not request.session.get('is_login',  None):
        return redirect('login')
    # 拿到人
    user_id = request.session.get('user_id')
    # 拿到时间
    now = datetime.datetime.now()
    day_num = now.isoweekday()
    week_day = now - datetime.timedelta(days=day_num)
    # 拿数据
    customers = Customer.objects.filter(user_id=user_id, created_at__range=(week_day, now))
    liaisons = Liaison.objects.filter(user_id=user_id, created_at__range=(week_day, now))
    records = Record.objects.filter(user_id=user_id, created_at__range=(week_day, now))
    businesses = Business.objects.filter(user_id=user_id, created_at__range=(week_day, now))
    print(customers, liaisons, records, businesses)
    return render(request, 'week.html', {
        'customers': customers,
        'liaisons': liaisons,
        'records': records,
        'businesses': businesses
    })


# def week_group(request):
#     """周数据汇总(团队)"""
#     if not request.session.get('is_login',  None):
#         return redirect('login')
#     # 拿到人
#     user_id = request.session.get('user_id')
#     users = User.objects.filter(up_name=user_id)
#
#     # 拿到时间
#     now = datetime.datetime.now()
#     day_num = now.isoweekday()
#     week_day = now - datetime.timedelta(days=day_num)
#     # 拿数据
#     # if 'name' in request.GET and request.GET['name']:
#     #     name = request.GET['name']
#     #     customers = Customer.objects.filter(name__icontains=name, user__up_name=up_name).exclude(is_valid=False)
#     # elif 'user_id' in request.GET and request.GET['user_id']:
#     #     user_id = request.GET['user_id']
#     #     customers = Customer.objects.filter(user=user_id, user__up_name=up_name).exclude(is_valid=False)
#     # else:
#     #     customers = Customer.objects.filter(user__up_name=up_name).exclude(is_valid=False)
#
#     customers = Customer.objects.filter(user_id=user_id, created_at__range=(week_day, now))
#     liaisons = Liaison.objects.filter(user_id=user_id, created_at__range=(week_day, now))
#     records = Record.objects.filter(user_id=user_id, created_at__range=(week_day, now))
#     businesses = Business.objects.filter(user_id=user_id, created_at__range=(week_day, now))
#
#     return render(request, 'week_group(暂时砍掉).html', {
#         'customers': customers,
#         'liaisons': liaisons,
#         'records': records,
#         'businesses': businesses,
#         'users': users
#     })


def week_all(request):
    """周数据汇总(全部)"""
    if not request.session.get('is_login',  None):
        return redirect('login')
    # 拿到人
    user_id = request.session.get('user_id')
    users = User.objects.all().exclude(role=3).exclude(role=5).exclude(pk=1)
    # 拿到时间
    now = datetime.datetime.now()
    day_num = now.isoweekday()
    week_day = now - datetime.timedelta(days=day_num)
    # 拿数据
    if 'user_id' in request.GET and request.GET['user_id']:
        user_id = request.GET['user_id']
        customers = Customer.objects.filter(user_id=user_id, created_at__range=(week_day, now)).exclude(is_valid=False)
        liaisons = Liaison.objects.filter(user_id=user_id, created_at__range=(week_day, now)).exclude(is_valid=False)
        records = Record.objects.filter(user_id=user_id, created_at__range=(week_day, now)).exclude(is_valid=False)
        businesses = Business.objects.filter(user_id=user_id, created_at__range=(week_day, now)).exclude(is_valid=False)
    else:
        customers = Customer.objects.filter(user_id=user_id, created_at__range=(week_day, now)).exclude(is_valid=False)
        liaisons = Liaison.objects.filter(user_id=user_id, created_at__range=(week_day, now)).exclude(is_valid=False)
        records = Record.objects.filter(user_id=user_id, created_at__range=(week_day, now)).exclude(is_valid=False)
        businesses = Business.objects.filter(user_id=user_id, created_at__range=(week_day, now)).exclude(is_valid=False)
    print(customers, liaisons, records, businesses)
    return render(request, 'week_all.html', {
        'customers': customers,
        'liaisons': liaisons,
        'records': records,
        'businesses': businesses,
        'users': users
    })
