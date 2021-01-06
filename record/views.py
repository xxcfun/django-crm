import xlwt
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views.generic import ListView

from customer.models import Customer
from record.forms import RecordForm
from record.models import Record
from users.models import User


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
    user_id = request.session.get('user_id')
    customers = Customer.objects.filter(user=user_id)
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
        'form': form,
        'customers': customers
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


def record_all(request):
    """所有拜访记录"""
    users = User.objects.all().exclude(role=3).exclude(role=5)
    if 'theme' in request.GET and request.GET['theme']:
        theme = request.GET['theme']
        records = Record.objects.filter(theme__icontains=theme).exclude(is_valid=False)
    elif 'user_id' in request.GET and request.GET['user_id']:
        user_id = request.GET['user_id']
        records = Record.objects.filter(user=user_id).exclude(is_valid=False)
    else:
        records = Record.objects.exclude(is_valid=False)
    paginator = Paginator(records, 10)
    page = request.GET.get('page')
    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        records = paginator.page(1)
    except EmptyPage:
        records = paginator.page(paginator.num_pages)
    return render(request, 'record_all.html', {
        'records': records,
        'users': users
    })


def record_all_detail(request, pk):
    """拜访记录详情"""
    record = get_object_or_404(Record, pk=pk, is_valid=True)
    form = RecordForm(instance=record)
    return render(request, 'record_all_detail.html', {
        'form': form,
    })


def export_record(request):
    """导出所有拜访记录信息"""
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="record.xls"'
    # 创建一个workbook，设置编码
    wb = xlwt.Workbook(encoding='utf-8')
    # 创建一个worksheet，对应excel中的sheet，表名称
    ws = wb.add_sheet('record')
    row_num = 0
    # 初始化样式
    font_style = xlwt.XFStyle()
    # 黑体
    font_style.font.bold = True
    # 写表头
    columns = ['拜访主题', '客户名称', '拜访方式', '主要事宜', '后续工作', '备注信息', '业务负责人', '创建时间']
    for col_num in range(len(columns)):
        # 参数解读：（行，列，值，样式），row行 col列
        ws.write(row_num, col_num, columns[col_num], font_style)
    # 写表格内容
    font_style = xlwt.XFStyle()
    font_style.font.bold = False
    rows = Record.objects.filter(is_valid=True).values_list('theme', 'customer__name', 'status', 'main', 'next', 'remarks', 'user__name', 'created_at')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    # 保存
    wb.save(response)
    return response
