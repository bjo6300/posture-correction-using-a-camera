from unicodedata import name
from django.urls import path

from . import views

app_name = 'posture'


urlpatterns = [
    # 메인페이지 "{% url 'posture:main' %}"
    path('', views.index, name='main'), 

    # 마이페이지 "{% url 'posture:mypage' %}"
    path('mypage/', views.mypage, name='mypage'),

    # 마이페이지 수정 "{% url 'posture:mypage_modify' %}"
    path('mypage_modify/', views.mypage_modify, name='mypage_modify'),

    # 회원가입 "{% url 'posture:signup' %}"
    path('signup/', views.signup, name='signup'),

    # 전체통계 "{% url 'posture:stats_all' %}"
    path('stats_all/', views.stats_all, name='stats_all'),

    # 거북목 통계 "{% url 'posture:stats_turtle_year' %}"
    path('stats_turtle_year/', views.stats_turtle_year, name='stats_turtle_year'),

    # 거북목 통계 "{% url 'posture:stats_shoulder_year' %}"
    path('stats_shoulder_year/', views.stats_shoulder_year, name='stats_shoulder_year'),

    
]