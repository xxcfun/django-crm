from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView

from liaison.forms import LiaisonForm
from liaison.models import Liaison


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
        'form': form
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
