from django.urls import path

from users import views

urlpatterns = [
    # 登录
    path('login/', views.login, name='login'),
    # 注销
    path('logout/', views.logout, name='logout'),
    # 个人中心
    path('mine/', views.mine, name='mine')
]
