from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from okr.forms import OkrForm
from okr.models import Okr


def okr(request):
    """okr展示"""
    user = request.session.get('user_id')
    okrs = Okr.objects.filter(user=user).exclude(is_valid=False)
    return render(request, 'okr.html', {
        'okrs': okrs
    })


def okr_add(request):
    """添加个人okr目标"""
    user_id = request.session.get('user_id')
    okr = Okr.objects.filter(user=user_id)
    if request.method == 'POST':
        form = OkrForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('okr')
        else:
            print(form.errors.as_json)
    else:
        form = OkrForm()
    return render(request, 'okr_add.html', {
        'okr': okr,
        'form': form
    })


def okr_edit(request, pk):
    """修改okr"""
    user = request.session.get('user_id')
    okr = get_object_or_404(Okr, pk=pk, user=user, is_valid=True)
    if request.method == 'POST':
        form = OkrForm(data=request.POST, instance=okr)
        if form.is_valid():
            form.save()
            return redirect('okr')
        else:
            print(form.errors.as_json)
    else:
        form = OkrForm(instance=okr)
    return render(request, 'okr_edit.html', {
        'form': form,
        'pk': pk
    })


def okr_finish(request, pk):
    """okr完成，即删除"""
    user = request.session.get('user_id')
    okr = get_object_or_404(Okr, pk=pk, user=user, is_valid=True)
    okr.delete()
    return redirect('okr')
