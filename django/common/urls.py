from django import views
from django.urls import path
from unicodedata import name
from django.contrib.auth import views as auth_views
from . import views
from .views import SignUpView

app_name = 'common'

urlpatterns = [
    
    # 로그인 "{% url 'common:login_main' %}"
    # path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login_main'), # 이건 관리자만 가능
    path('login/', views.login_main, name='login_main'),

    # 로그아웃 "{% url 'common:logout' %}"
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # 아이디 찾기 "{% url 'common:find_id' %}"
    path('find_id/', views.find_id, name='find_id'),

    # 아이디 찾기 체크완료 "{% url 'common:find_id_checked' %}"
    path('find_id/checked', views.find_id_checked, name='find_id_checked'),

    # 회원가입 페이지
    path('signup/', SignUpView.as_view(), name='signup'),
    
    # 회원가입 완료 페이지 "{% url 'common:signup_completed' %}"
    path('signup/completed', views.signup_completed, name='signup_completed'),  

    # 비밀번호 수정 "{% url 'common:modify_password' %}"
    path('modify_password/', views.modify_password, name='modify_password'),

    # 비밀번호 수정 "{% url 'common:modify_password_completed' %}"
    path('modify_password_completed/', views.modify_password_completed, name='modify_password_completed'),
]