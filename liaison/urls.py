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
]