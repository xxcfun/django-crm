from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from customer.forms import CustomerForm, CustomerShopForm, CustomerInvoiceForm
from customer.models import Customer, CustomerShop, CustomerInvoice
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

    return render(request, 'customer_detail.html', {
        'form': form,
        'pk': pk,
        'shopform': shopform,
        'invoiceform': invoiceform
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
    return render(request, 'customer_all_detail.html', {
        'form': form,
        'pk': pk,
        'shopform': shopform,
        'invoiceform': invoiceform
    })
