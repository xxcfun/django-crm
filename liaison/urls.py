from django.urls import path

from liaison import views
from liaison.views import LiaisonView

urlpatterns = [
    # 查看联系人
    path('', LiaisonView.as_view(), name='liaison'),
    # 添加联系人
    path('add/', views.liaison_add, name='liaison_add'),
    # 查看和修改联系人
    path('detail/<int:pk>', views.liaison_detail, name='liaison_detail'),
    # 单个页面进行修改
    path('edit/<int:pk>', views.liaison_edit, name='liaison_edit'),
    # 删除联系人
    path('delete/<int:pk>', views.liaison_delete, name='liaison_delete'),

    # 团队联系人
    path('group/', views.liaison_group, name='liaison_group'),

    # 所有联系人列表
    path('all/', views.liaison_all, name='liaison_all'),
    # 客户详情
    path('all/detail/<int:pk>', views.liaison_all_detail, name='liaison_all_detail'),

    # 导出所有联系人信息
    path('export/liaison', views.export_liaison, name='export_liaison'),
]