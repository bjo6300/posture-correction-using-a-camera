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

    # 전체통계 "{% url 'posture:stats_all_month' %}"
    path('stats_all_month/', views.stats_all_month, name='stats_all_month'),

    # 거북목 월간통계 "{% url 'posture:stats_turtle_month' %}"
    path('stats_turtle_month/', views.stats_turtle_month, name='stats_turtle_month'),

    # 거북목 주간통계 "{% url 'posture:stats_turtle_week' %}"
    path('stats_turtle_week/', views.stats_turtle_week, name='stats_turtle_week'),

    # 거북목 일간통계 "{% url 'posture:stats_turtle_day' %}"
    path('stats_turtle_day/', views.stats_turtle_day, name='stats_turtle_day'),

    # 어깨비대칭 월간통계 "{% url 'posture:stats_shoulder_month' %}"
    path('stats_shoulder_month/', views.stats_shoulder_month, name='stats_shoulder_month'),

    # 턱괴기 월간통계 "{% url 'posture:stats_jaw_month' %}"
    path('stats_jaw_month/', views.stats_jaw_month, name='stats_jaw_month'),
    
]