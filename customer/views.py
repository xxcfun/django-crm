import xlwt
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from business.forms import BusinessForm
from business.models import Business
from customer.forms import CustomerForm, CustomerShopForm, CustomerInvoiceForm
from customer.models import Customer, CustomerShop, CustomerInvoice
from liaison.forms import LiaisonForm
from liaison.models import Liaison
from record.forms import RecordForm
from record.models import Record
from users.models import User


class CustomerView(ListView):
    """客户列表"""
    model = Customer
    template_name = 'customer.html'
    paginate_by = 10
    context_object_name = 'customers'

    def get_queryset(self):
        user = self.request.session.get('user_id')
        if 'name' in self.request.GET and self.request.GET['name']:
            name = self.request.GET['name']
            return Customer.objects.filter(name__icontains=name, user=user, is_valid=True)
        if 'rank' in self.request.GET and self.request.GET['rank']:
            rank = self.request.GET['rank']
            return Customer.objects.filter(rank=rank, user=user, is_valid=True)
        if 'industry' in self.request.GET and self.request.GET['industry']:
            industry = self.request.GET['industry']
            return Customer.objects.filter(industry=industry, user=user, is_valid=True)
        else:
            return Customer.objects.filter(is_valid=True, user=user)


def customer_add(request):
    """客户添加"""
    if request.method == 'POST':
        form = CustomerForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer')
        else:
            print(form.errors.as_json)
    else:
        form = CustomerForm()
    return render(request, 'customer_add.html', {
        'form': form
    })


def customer_detail(request, pk):
    """客户详情（外带地址信息）"""
    user = request.session.get('user_id')
    customer = get_object_or_404(Customer, pk=pk, user=user, is_valid=True)
    if request.method == 'POST':
        form = CustomerForm(data=request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_detail', pk)
        else:
            print(form.errors.as_json)
    else:
        form = CustomerForm(instance=customer)
    # 添加上地址信息
    # 下面这里引入异常处理，如果数据库里没有该字段，那么表单渲染为空
    try:
        customer_shop = CustomerShop.objects.get(customer=pk)
        shopform = CustomerShopForm(instance=customer_shop)
    except CustomerShop.DoesNotExist:
        shopform = CustomerShopForm()

    try:
        customer_invoice = CustomerInvoice.objects.get(customer=pk)
        invoiceform = CustomerInvoiceForm(instance=customer_invoice)
    except CustomerInvoice.DoesNotExist:
        invoiceform = CustomerInvoiceForm()

    # 添加联系人，商机，拜访记录信息
    liaisons = Liaison.objects.filter(customer_id=pk, is_valid=True)
    records = Record.objects.filter(customer_id=pk, is_valid=True)
    businesses = Business.objects.filter(customer_id=pk, is_valid=True)

    return render(request, 'customer_detail.html', {
        'form': form,
        'pk': pk,
        'shopform': shopform,
        'invoiceform': invoiceform,
        'liaisons': liaisons,
        'records': records,
        'businesses': businesses
    })


def customer_edit(request, pk):
    """客户编辑"""
    user = request.session.get('user_id')
    customer = get_object_or_404(Customer, pk=pk, user=user, is_valid=True)
    if request.method == 'POST':
        form = CustomerForm(data=request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer')
        else:
            print(form.errors.as_json)
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customer_edit.html', {
        'form': form,
        'pk': pk
    })


def customer_delete(request, pk):
    """客户删除"""
    user = request.session.get('user_id')
    customer = get_object_or_404(Customer, pk=pk, user=user, is_valid=True)
    customer.delete()
    return redirect('customer')


def address_shop(request, pk):
    """客户收货地址"""
    shopform = CustomerShopForm(data=request.POST)
    if shopform.is_valid():
        shopform.save()
    else:
        print(shopform.errors.as_json)
    return redirect('customer_detail', pk)


def address_invoice(request, pk):
    """客户发票地址"""
    invoiceform = CustomerInvoiceForm(data=request.POST)
    if invoiceform.is_valid():
        invoiceform.save()
    else:
        print(invoiceform.errors.as_json)
    return redirect('customer_detail', pk)


def customer_group(request):
    """团队客户，可筛选"""
    up_name = request.session.get('user_id')
    users = User.objects.filter(up_name=up_name)
    if 'name' in request.GET and request.GET['name']:
        name = request.GET['name']
        customers = Customer.objects.filter(name__icontains=name, user__up_name=up_name).exclude(is_valid=False)
    elif 'user_id' in request.GET and request.GET['user_id']:
        user_id = request.GET['user_id']
        customers = Customer.objects.filter(user=user_id, user__up_name=up_name).exclude(is_valid=False)
    else:
        customers = Customer.objects.filter(user__up_name=up_name).exclude(is_valid=False)
    paginator = Paginator(customers, 10)
    page = request.GET.get('page')
    try:
        customers = paginator.page(page)
    except PageNotAnInteger:
        customers = paginator.page(1)
    except EmptyPage:
        customers = paginator.page(paginator.num_pages)
    return render(request, 'customer_all.html', {
        'customers': customers,
        'users': users
    })


def customer_all(request):
    """所有客户，可筛选"""
    users = User.objects.all().exclude(role=3).exclude(role=5)
    if 'name' in request.GET and request.GET['name']:
        name = request.GET['name']
        customers = Customer.objects.filter(name__icontains=name).exclude(is_valid=False)
    elif 'user_id' in request.GET and request.GET['user_id']:
        user_id = request.GET['user_id']
        customers = Customer.objects.filter(user=user_id).exclude(is_valid=False)
    else:
        customers = Customer.objects.exclude(is_valid=False)
    paginator = Paginator(customers, 10)
    page = request.GET.get('page')
    try:
        customers = paginator.page(page)
    except PageNotAnInteger:
        customers = paginator.page(1)
    except EmptyPage:
        customers = paginator.page(paginator.num_pages)
    return render(request, 'customer_all.html', {
        'customers': customers,
        'users': users
    })


def customer_all_detail(request, pk):
    """客户详情（不能更改信息）"""
    customer = get_object_or_404(Customer, pk=pk, is_valid=True)
    form = CustomerForm(instance=customer)
    # 添加上地址信息
    # 下面这里引入异常处理，如果数据库里没有该字段，那么表单渲染为空
    try:
        customer_shop = CustomerShop.objects.get(customer=pk)
        shopform = CustomerShopForm(instance=customer_shop)
    except CustomerShop.DoesNotExist:
        shopform = CustomerShopForm()

    try:
        customer_invoice = CustomerInvoice.objects.get(customer=pk)
        invoiceform = CustomerInvoiceForm(instance=customer_invoice)
    except CustomerInvoice.DoesNotExist:
        invoiceform = CustomerInvoiceForm()

    # 添加联系人，商机，拜访记录信息
    liaisons = Liaison.objects.filter(customer_id=pk, is_valid=True)
    records = Record.objects.filter(customer_id=pk, is_valid=True)
    businesses = Business.objects.filter(customer_id=pk, is_valid=True)

    return render(request, 'customer_all_detail.html', {
        'form': form,
        'pk': pk,
        'shopform': shopform,
        'invoiceform': invoiceform,
        'liaisons': liaisons,
        'records': records,
        'businesses': businesses
    })


def export_customer(request):
    """导出所有客户信息"""
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="customer.xls"'
    # 创建一个workbook，设置编码
    wb = xlwt.Workbook(encoding='utf-8')
    # 创建一个worksheet，对应excel中的sheet，表名称
    ws = wb.add_sheet('customer')
    row_num = 0
    # 初始化样式
    font_style = xlwt.XFStyle()
    # 黑体
    font_style.font.bold = True
    # 写表头
    columns = ['客户名称', '级别', '网址', '规模', '性质', '行业', '备注信息', '业务负责人', '创建时间']
    for col_num in range(len(columns)):
        # 参数解读：（行，列，值，样式），row行 col列
        ws.write(row_num, col_num, columns[col_num], font_style)
    # 写表格内容
    font_style = xlwt.XFStyle()
    font_style.font.bold = False
    rows = Customer.objects.filter(is_valid=True).values_list('name', 'rank', 'website', 'scale', 'nature', 'industry', 'remarks', 'user__name', 'created_at')
    for row in rows:
        # # 目前这些有问题，会报元组错误
        # # rank
        # if row[1] == 1:
        #     row[1] = '重点客户'
        # elif row[1] == 2:
        #     row[1] = '一般客户'
        # elif row[1] == 3:
        #     row[1] = '普通客户'
        # # scale
        # if row[3] == 1:
        #     row[3] = '0~10人'
        # elif row[3] == 2:
        #     row[3] = '10~50人'
        # elif row[3] == 3:
        #     row[3] = '50~100人'
        # elif row[3] == 4:
        #     row[3] = '100~1000人'
        # elif row[3] == 5:
        #     row[3] = '1000人及以上'
        # # nature
        # if row[4] == 1:
        #     row[4] = '有限责任公司'
        # elif row[4] == 2:
        #     row[4] = '股份有限公司'
        # elif row[4] == 3:
        #     row[4] = '国有企业'
        # elif row[4] == 4:
        #     row[4] = '集体企业'
        # elif row[4] == 5:
        #     row[4] = '私营企业'
        # elif row[4] == 6:
        #     row[4] = '个体工商户'
        # elif row[4] == 7:
        #     row[4] = '合伙企业'
        # elif row[4] == 8:
        #     row[4] = '联营企业'
        # elif row[4] == 9:
        #     row[4] = '股份合作制企业'
        # # industry
        # if row[5] == 1:
        #     row[5] = '机台设备制造商'
        # elif row[5] == 2:
        #     row[5] = '生产制造型企业'
        # elif row[5] == 3:
        #     row[5] = '系统集成商'
        # elif row[5] == 4:
        #     row[5] = '分销商'
        # elif row[5] == 5:
        #     row[5] = '其它'
        # # user
        # row[7] = user_name
        # 下面开始写表格内容
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    # 保存
    wb.save(response)
    return response


def customer_add_liaison(request, pk):
    """客户详情里添加联系人"""
    customer = get_object_or_404(Customer, pk=pk, is_valid=True)
    if request.method == 'POST':
        form = LiaisonForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_detail', pk)
        else:
            print(form.errors.as_json)
    else:
        form = LiaisonForm()
    return render(request, 'customer_add_liaison.html', {
        'form': form,
        'customer': customer,
        'pk': pk,
    })


def customer_add_record(request, pk):
    """客户详情里添加拜访记录"""
    customer = get_object_or_404(Customer, pk=pk, is_valid=True)
    if request.method == 'POST':
        form = RecordForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_detail', pk)
        else:
            print(form.errors.as_json)
    else:
        form = RecordForm()
    return render(request, 'customer_add_record.html', {
        'form': form,
        'customer': customer,
        'pk': pk,
    })


def customer_add_business(request, pk):
    """客户详情里添加商机"""
    customer = get_object_or_404(Customer, pk=pk, is_valid=True)
    if request.method == 'POST':
        form = BusinessForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_detail', pk)
        else:
            print(form.errors.as_json)
    else:
        form = BusinessForm()
    return render(request, 'customer_add_business.html', {
        'form': form,
        'customer': customer,
        'pk': pk,
    })


def customer_edit_liaison(request, pk):
    """客户详情里修改联系人"""
    user = request.session.get('user_id')
    liaison = get_object_or_404(Liaison, pk=pk, user=user, is_valid=True)
    if request.method == 'POST':
        form = LiaisonForm(data=request.POST, instance=liaison)
        if form.is_valid():
            form.save()
            return redirect('customer_detail', liaison.customer.pk)
        else:
            print(form.errors.as_json)
    else:
        form = LiaisonForm(instance=liaison)
    return render(request, 'customer_edit_liaison.html', {
        'form': form,
        'liaison': liaison,
        'pk': pk,
    })


def customer_edit_record(request, pk):
    """客户详情里修改拜访记录"""
    user = request.session.get('user_id')
    record = get_object_or_404(Record, pk=pk, user=user, is_valid=True)
    if request.method == 'POST':
        form = RecordForm(data=request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('customer_detail', record.customer.pk)
        else:
            print(form.errors.as_json)
    else:
        form = RecordForm(instance=record)
    return render(request, 'customer_edit_record.html', {
        'form': form,
        'record': record,
        'pk': pk,
    })


def customer_edit_business(request, pk):
    """客户详情里修改商机"""
    user = request.session.get('user_id')
    business = get_object_or_404(Business, pk=pk, user=user, is_valid=True)
    if request.method == 'POST':
        form = BusinessForm(data=request.POST, instance=business)
        if form.is_valid():
            form.save()
            return redirect('customer_detail', business.customer.pk)
        else:
            print(form.errors.as_json)
    else:
        form = BusinessForm(instance=business)
    return render(request, 'customer_edit_business.html', {
        'form': form,
        'business': business,
        'pk': pk,
    })


def customer_delete_liaison(request, pk):
    """客户详情里删除联系人"""
    user = request.session.get('user_id')
    liaison = get_object_or_404(Liaison, pk=pk, user=user, is_valid=True)
    liaison.delete()
    return redirect('customer_detail', liaison.customer.pk)


def customer_delete_record(request, pk):
    """客户详情里删除拜访记录"""
    user = request.session.get('user_id')
    record = get_object_or_404(Record, pk=pk, user=user, is_valid=True)
    record.delete()
    return redirect('customer_detail', record.customer.pk)


def customer_delete_business(request, pk):
    """客户详情里删除商机"""
    user = request.session.get('user_id')
    business = get_object_or_404(Business, pk=pk, user=user, is_valid=True)
    business.delete()
    return redirect('customer_detail', business.customer.pk)


def customer_detail_liaison(request, pk):
    """客户详情里查看联系人"""
    liaison = get_object_or_404(Liaison, pk=pk, is_valid=True)
    form = LiaisonForm(instance=liaison)
    return render(request, 'customer_detail_liaison.html', {
        'form': form,
        'liaison': liaison
    })


def customer_detail_record(request, pk):
    """客户详情里查看拜访记录"""
    record = get_object_or_404(Record, pk=pk, is_valid=True)
    form = RecordForm(instance=record)
    return render(request, 'customer_detail_record.html', {
        'form': form,
        'record': record
    })


def customer_detail_business(request, pk):
    """客户详情里查看商机"""
    business = get_object_or_404(Business, pk=pk, is_valid=True)
    form = BusinessForm(instance=business)
    return render(request, 'customer_detail_business.html', {
        'form': form,
        'business': business
    })
