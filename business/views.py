from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views.generic import ListView

from business.forms import BusinessForm
from business.models import Business


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
        'form': form
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
