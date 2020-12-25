from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views.generic import ListView

from record.forms import RecordForm
from record.models import Record


class RecordView(ListView):
    """拜访记录列表"""
    model = Record
    template_name = 'record.html'
    paginate_by = 10
    context_object_name = 'records'

    def get_queryset(self):
        user = self.request.session.get('user_id')
        if 'name' in self.request.GET and self.request.GET['name']:
            name = self.request.GET['name']
            return Record.objects.filter(customer__name__icontains=name, user=user, is_valid=True)
        else:
            return Record.objects.filter(user=user, is_valid=True)


def record_add(request):
    """拜访记录添加"""
    if request.method == 'POST':
        form = RecordForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('record')
        else:
            print(form.errors.as_json)
    else:
        form = RecordForm()
    return render(request, 'record_add.html', {
        'form': form
    })


def record_detail(request, pk):
    """拜访记录详情"""
    user = request.session.get('user_id')
    record = get_object_or_404(Record, pk=pk, user=user, is_valid=True)
    if request.method == 'POST':
        form = RecordForm(data=request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('record_detail', pk)
        else:
            print(form.errors.as_json)
    else:
        form = RecordForm(instance=record)
    return render(request, 'record_detail.html', {
        'form': form,
        'pk': pk
    })


def record_edit(request, pk):
    """拜访记录修改"""
    user = request.session.get('user_id')
    record = get_object_or_404(Record, pk=pk, user=user, is_valid=True)
    if request.method == 'POST':
        form = RecordForm(data=request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('record')
        else:
            print(form.errors.as_json)
    else:
        form = RecordForm(instance=record)
    return render(request, 'record_edit.html', {
        'form': form,
        'pk': pk
    })


def record_delete(request, pk):
    """拜访记录删除"""
    user = request.session.get('user_id')
    record = get_object_or_404(Record, pk=pk, user=user, is_valid=True)
    record.delete()
    return redirect('record')
