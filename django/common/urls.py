from django import views
from django.urls import path
from unicodedata import name
from django.contrib.auth import views as auth_views
from . import views

app_name = 'common'

urlpatterns = [
    
    # 로그인 "{% url 'common:login' %}"
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),

    # 로그아웃 "{% url 'common:logout' %}"
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # 아이디 찾기 "{% url 'common:find_id' %}"
    path('find_id/', views.find_id, name='find_id'),
]