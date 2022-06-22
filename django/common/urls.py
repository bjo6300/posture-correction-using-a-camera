from django import views
from django.urls import path, reverse_lazy
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

    # 비밀번호 초기화
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

# from django.urls import reverse_lazy

    # path('password_reset/', auth_views.PasswordResetView.as_view(success_url=reverse_lazy('common:password_reset_done')), name='password_reset'),
    # path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # # path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('common:password_reset_complete')), name='password_reset_confirm'),
    # path('rest-auth/password/reset/confirm/<str:uidb64>/<str:token>', auth_views.PasswordResetConfirmView.as_view(),
    #         name='password_reset_confirm'),
    # path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),



    # 회원가입 페이지
    path('signup/', SignUpView.as_view(), name='signup'),
    
    # 회원가입 완료 페이지 "{% url 'common:signup_completed' %}"
    path('signup/completed', views.signup_completed, name='signup_completed'),  

    # 비밀번호 수정 "{% url 'common:change_password' %}"
    path('change_password/', views.change_password, name='change_password'),

    # 비밀번호 수정 완료 "{% url 'common:modify_password_completed' %}"
    path('modify_password_completed/', views.modify_password_completed, name='modify_password_completed'),

    # 이메일 수정 "{% url 'common:modify_email' %}"
    path('modify_email/', views.modify_email, name='modify_email'),

    # 이메일 수정 "{% url 'common:modify_email_completed' %}"
    path('modify_email_completed/', views.modify_email_completed, name='modify_email_completed'),

]