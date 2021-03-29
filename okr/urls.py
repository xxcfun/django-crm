from django.urls import path

from okr import views

urlpatterns = [
    path('', views.okr, name='okr'),
    # 添加个人okr目标
    path('add/', views.okr_add, name='okr_add'),
    # 修改个人okr目标
    path('edit/<int:pk>', views.okr_edit, name='okr_edit'),
    # 完成个人okr目标，即讲该字段删除
    path('finish/<int:pk>', views.okr_finish, name='okr_finish'),
]