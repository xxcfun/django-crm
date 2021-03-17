from django.urls import path

from business import views
from business.views import BusinessView

urlpatterns = [
    # 查看商机
    path('', BusinessView.as_view(), name='business'),
    # 添加商机
    path('add/', views.business_add, name='business_add'),
    # 查看和修改商机
    path('detail/<int:pk>', views.business_detail, name='business_detail'),
    # 单个页面进行修改
    path('edit/<int:pk>', views.business_edit, name='business_edit'),
    # 删除商机
    path('delete/<int:pk>', views.business_delete, name='business_delete'),

    # 团队所有商机
    path('group/', views.business_group, name='business_group'),

    # 所有商机列表
    path('all/', views.business_all, name='business_all'),
    # 客户详情
    path('all/detail/<int:pk>', views.business_all_detail, name='business_all_detail'),

    # 导出所有商机信息
    path('export/business', views.export_business, name='export_business'),
]