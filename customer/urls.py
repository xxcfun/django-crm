from django.urls import path, include

from customer import views
from customer.views import CustomerView

urlpatterns = [
    # 查看客户
    path('', CustomerView.as_view(), name='customer'),
    # 添加客户
    path('add/', views.customer_add, name='customer_add'),
    # 查看和修改客户
    path('detail/<int:pk>', views.customer_detail, name='customer_detail'),
    # 单个页面进行修改
    path('edit/<int:pk>', views.customer_edit, name='customer_edit'),
    # 删除客户
    path('delete/<int:pk>', views.customer_delete, name='customer_delete'),

    # 客户信息的地址维护
    # 客户收货地址
    path('address/shop/<int:pk>', views.address_shop, name='address_shop'),
    # 客户发票地址
    path('address/invoice/<int:pk>', views.address_invoice, name='address_invoice'),

    # 团队所有客户
    path('group/', views.customer_group, name='customer_group'),

    # 所有客户列表
    path('all/', views.customer_all, name='customer_all'),
    # 客户详情
    path('all/detail/<int:pk>', views.customer_all_detail, name='customer_all_detail'),

    # 导出所有客户信息
    path('export/customer', views.export_customer, name='export_customer'),

    # 下面全都是在客户详情里面的操作
    # 客户详情页添加联系人
    path('detail/<int:pk>/add/liaison', views.customer_add_liaison, name='customer_add_liaison'),
    # 客户详情页添加拜访记录
    path('detail/<int:pk>/add/record', views.customer_add_record, name='customer_add_record'),
    # 客户详情页添加商机
    path('detail/<int:pk>/add/business', views.customer_add_business, name='customer_add_business'),

    # 客户详情页修改联系人
    path('detail/<int:pk>/edit/liaison', views.customer_edit_liaison, name='customer_edit_liaison'),
    # 客户详情页修改拜访记录
    path('detail/<int:pk>/edit/record', views.customer_edit_record, name='customer_edit_record'),
    # 客户详情页修改商机
    path('detail/<int:pk>/edit/business', views.customer_edit_business, name='customer_edit_business'),

    # 客户详情页删除联系人
    path('detail/<int:pk>/delete/liaison', views.customer_delete_liaison, name='customer_delete_liaison'),
    # 客户详情页删除拜访记录
    path('detail/<int:pk>/delete/record', views.customer_delete_record, name='customer_delete_record'),
    # 客户详情页删除商机
    path('detail/<int:pk>/delete/business', views.customer_delete_business, name='customer_delete_business'),

    # 客户详情页查看联系人
    path('detail/<int:pk>/detail/liaison', views.customer_detail_liaison, name='customer_detail_liaison'),
    # 客户详情页查看拜访记录
    path('detail/<int:pk>/detail/record', views.customer_detail_record, name='customer_detail_record'),
    # 客户详情页查看商机
    path('detail/<int:pk>/detail/business', views.customer_detail_business, name='customer_detail_business'),
]
