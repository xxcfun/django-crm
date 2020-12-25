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
    path('address/invoice/<int:pk>', views.address_invoice, name='address_invoice')
]
