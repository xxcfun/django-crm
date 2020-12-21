from django.urls import path, include

from customer import views
from customer.views import CustomerView

urlpatterns = [
    # 查看客户
    path('', CustomerView.as_view(), name='customer'),
    # 根据筛选用户查看客户
    path('seach/', views.customer_seach, name='customer_seach'),
    # 添加客户
    path('add/', views.customer_add, name='customer_add'),
    # 查看和修改客户
    path('detail/<int:pk>', views.customer_detail, name='customer_detail'),
    # 单个页面进行修改
    path('edit/<int:pk>', views.customer_edit, name='customer_edit'),
    # 删除客户
    path('delete/<int:pk>', views.customer_delete, name='customer_delete'),
    #
]
