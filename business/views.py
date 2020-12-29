from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views.generic import ListView

from business.forms import BusinessForm
from business.models import Business
from customer.models import Customer
from users.models import User


class BusinessView(ListView):
    """商机列表"""
    model = Business
    template_name = 'business.html'
    paginate_by = 10
    context_object_name = 'businesses'

    def get_queryset(self):
        user = self.request.session.get('user_id')
        if 'name' in self.request.GET and self.request.GET['name']:
            name = self.request.GET['name']
            return Business.objects.filter(name__icontains=name, user=user, is_valid=True)
        else:
            return Business.objects.filter(user=user, is_valid=True)


def business_add(request):
    """商机添加"""
    user_id = request.session.get('user_id')
    customers = Customer.objects.filter(user=user_id)
    if request.method == 'POST':
        form = BusinessForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('business')
        else:
            print(form.errors.as_json)
    else:
        form = BusinessForm()
    return render(request, 'business_add.html', {
        'form': form,
        'customers': customers
    })


def business_detail(request, pk):
    """商机详情"""
    user = request.session.get('user_id')
    business = get_object_or_404(Business, pk=pk, user=user, is_valid=True)
    if request.method == 'POST':
        form = BusinessForm(data=request.POST, instance=business)
        if form.is_valid():
            form.save()
            return redirect('business_detail', pk)
        else:
            print(form.errors.as_json)
    else:
        form = BusinessForm(instance=business)
    return render(request, 'business_detail.html', {
        'form': form,
        'pk': pk
    })


def business_edit(request, pk):
    """商机修改"""
    user = request.session.get('user_id')
    business = get_object_or_404(Business, pk=pk, user=user, is_valid=True)
    if request.method == 'POST':
        form = BusinessForm(data=request.POST, instance=business)
        if form.is_valid():
            form.save()
            return redirect('business')
        else:
            print(form.errors.as_json)
    else:
        form = BusinessForm(instance=business)
    return render(request, 'business_edit.html', {
        'form': form,
        'pk': pk
    })


def business_delete(request, pk):
    """商机删除"""
    user = request.session.get('user_id')
    business = get_object_or_404(Business, pk=pk, user=user, is_valid=True)
    business.delete()
    return redirect('business')


def business_all(request):
    # 所有商机
    users = User.objects.all().exclude(role=3).exclude(role=5)
    if 'name' in request.GET and request.GET['name']:
        name = request.GET['name']
        businesses = Business.objects.filter(name__icontains=name).exclude(is_valid=False)
    elif 'user_id' in request.GET and request.GET['user_id']:
        user_id = request.GET['user_id']
        businesses = Business.objects.filter(user=user_id).exclude(is_valid=False)
    else:
        businesses = Business.objects.exclude(is_valid=False)
    paginator = Paginator(businesses, 10)
    page = request.GET.get('page')
    try:
        businesses = paginator.page(page)
    except PageNotAnInteger:
        businesses = paginator.page(1)
    except EmptyPage:
        businesses = paginator.page(paginator.num_pages)
    return render(request, 'business_all.html', {
        'businesses': businesses,
        'users': users
    })


def business_all_detail(request, pk):
    # 商机详情
    business = get_object_or_404(Business, pk=pk, is_valid=True)
    form = BusinessForm(instance=business)
    return render(request, 'business_all_detail.html', {
        'form': form,
    })
