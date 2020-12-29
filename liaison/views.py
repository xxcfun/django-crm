from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView

from customer.models import Customer
from liaison.forms import LiaisonForm
from liaison.models import Liaison
from users.models import User


class LiaisonView(ListView):
    """联系人列表"""
    model = Liaison
    template_name = 'liaison.html'
    paginate_by = 10
    context_object_name = 'liaisons'

    def get_queryset(self):
        user = self.request.session.get('user_id')
        if 'name' in self.request.GET and self.request.GET['name']:
            name = self.request.GET['name']
            return Liaison.objects.filter(name__icontains=name, user=user, is_valid=True )
        else:
            return Liaison.objects.filter(user=user, is_valid=True)


def liaison_add(request):
    """联系人添加"""
    user_id = request.session.get('user_id')
    customers = Customer.objects.filter(user=user_id)
    if request.method == 'POST':
        form = LiaisonForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('liaison')
        else:
            print(form.errors.as_json)
    else:
        form = LiaisonForm()
    return render(request, 'liaison_add.html', {
        'form': form,
        'customers': customers
    })


def liaison_detail(request, pk):
    """联系人详情"""
    user = request.session.get('user_id')
    liaison = get_object_or_404(Liaison, pk=pk, user=user, is_valid=True)
    if request.method == 'POST':
        form = LiaisonForm(data=request.POST, instance=liaison)
        if form.is_valid():
            form.save()
            return redirect('liaison_detail', pk)
        else:
            print(form.errors.as_json)
    else:
        form = LiaisonForm(instance=liaison)
    return render(request, 'liaison_detail.html', {
        'form': form,
        'pk': pk
    })


def liaison_edit(request, pk):
    """联系人修改"""
    user = request.session.get('user_id')
    liaison = get_object_or_404(Liaison, pk=pk, user=user, is_valid=True)
    if request.method == 'POST':
        form = LiaisonForm(data=request.POST, instance=liaison)
        if form.is_valid():
            form.save()
            return redirect('liaison')
        else:
            print(form.errors.as_json)
    else:
        form = LiaisonForm(instance=liaison)
    return render(request, 'liaison_edit.html', {
        'form': form,
        'pk': pk
    })


def liaison_delete(request, pk):
    """联系人删除"""
    user = request.session.get('user_id')
    liaison = get_object_or_404(Liaison, pk=pk, user=user, is_valid=True)
    liaison.delete()
    return redirect('liaison')


def liaison_all(request):
    """所有联系人"""
    users = User.objects.all().exclude(role=3).exclude(role=5)
    if 'name' in request.GET and request.GET['name']:
        name = request.GET['name']
        liaisons = Liaison.objects.filter(name__icontains=name).exclude(is_valid=False)
    elif 'user_id' in request.GET and request.GET['user_id']:
        user_id = request.GET['user_id']
        liaisons = Liaison.objects.filter(user=user_id).exclude(is_valid=False)
    else:
        liaisons = Liaison.objects.exclude(is_valid=False)
    paginator = Paginator(liaisons, 10)
    page = request.GET.get('page')
    try:
        liaisons = paginator.page(page)
    except PageNotAnInteger:
        liaisons = paginator.page(1)
    except EmptyPage:
        liaisons = paginator.page(paginator.num_pages)
    return render(request, 'liaison_all.html', {
        'liaisons': liaisons,
        'users': users
    })


def liaison_all_detail(request, pk):
    """联系人详情"""
    liaison = get_object_or_404(Liaison, pk=pk, is_valid=True)
    form = LiaisonForm(instance=liaison)
    return render(request, 'liaison_all_detail.html', {
        'form': form,
    })
