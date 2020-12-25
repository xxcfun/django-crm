from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from customer.forms import CustomerForm, CustomerShopForm, CustomerInvoiceForm
from customer.models import Customer, CustomerShop, CustomerInvoice


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
    customer_shop = get_object_or_404(CustomerShop, customer=pk)
    shopform = CustomerShopForm(instance=customer_shop)
    customer_invoice = get_object_or_404(CustomerInvoice, customer=pk)
    invoiceform = CustomerInvoiceForm(instance=customer_invoice)
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
    customer_shop = get_object_or_404(CustomerShop, customer=pk)
    if request.method == 'POST':
        shopform = CustomerShopForm(data=request.POST, instance=customer_shop)
        if shopform.is_valid():
            shopform.save()
            return redirect('customer_detail', pk)
        else:
            print(shopform.errors.as_json)
    else:
        shopform = CustomerShopForm(instance=customer_shop)
    return render(request, 'customer_detail.html', {
        'shopform': shopform,
        'pk': pk
    })


def address_invoice(request, pk):
    """客户发票地址"""
    customer_invoice = get_object_or_404(CustomerInvoice, customer=pk)
    if request.method == 'POST':
        invoiceform = CustomerInvoiceForm(data=request.POST, instance=customer_invoice)
        if invoiceform.is_valid():
            invoiceform.save()
            return redirect('customer_detail', pk)
        else:
            print(invoiceform.errors.as_json)
    else:
        invoiceform = CustomerInvoiceForm(instance=customer_invoice)
    return render(request, 'customer_detail.html', {
        'invoiceform': invoiceform,
        'pk': pk
    })
