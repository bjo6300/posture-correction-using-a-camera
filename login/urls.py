from django.urls import path
from django.contrib.auth import views as auth_views

from login import views

app_name = 'login'

urlpatterns = [
    # path('', auth_views.LoginView.as_view(template_name='login:login.html'), name='login'),
    path('', views.login, name='login'), # 로그인 메인 페이지
]