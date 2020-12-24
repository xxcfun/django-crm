from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from customer.forms import CustomerForm
from customer.models import Customer


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
        if form.is_valid:
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
    """客户详情"""
    user = request.session.get('user_id')
    customer = get_object_or_404(Customer, pk=pk, user=user, is_valid=True)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return render(request, 'customer_detail.html', {
                'form': form,
                'pk': pk
            })
        else:
            print(form.errors.as_json)
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customer_detail.html', {
        'form': form,
        'pk': pk
    })


def customer_edit(request, pk):
    """客户编辑"""
    user = request.session.get('user_id')
    customer = get_object_or_404(Customer, pk=pk, user=user, is_valid=True)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
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
