from unicodedata import name
from django.urls import path

from . import views

app_name = 'posture'


urlpatterns = [
    # 메인페이지 "{% url 'posture:main' %}"
    path('', views.index, name='main'), 

    # 메인페이지 - 프로그램 시작 "{% url 'posture:program' %}"
    path('program/', views.program, name='program'),

    # 마이페이지 "{% url 'posture:mypage' %}"
    path('mypage/', views.mypage, name='mypage'),

    # 마이페이지 수정 "{% url 'posture:mypage_modify' %}"
    path('mypage_modify/', views.mypage_modify, name='mypage_modify'),

    # 거북목 추천 영상 "{% url 'posture:recommended_turtle' %}"
    path('recommended_turtle/', views.recommended_turtle, name='recommended_turtle'),

    # 어깨비대칭 추천 영상 "{% url 'posture:recommended_shoulder' %}"
    path('recommended_shoulder/', views.recommended_shoulder, name='recommended_shoulder'),

    # 턱괴기 추천 영상 "{% url 'posture:recommended_jaw' %}"
    path('recommended_jaw/', views.recommended_jaw, name='recommended_jaw'),

    # 전체 월간 통계 "{% url 'posture:stats_all_month' %}"
    path('stats_all_month/', views.stats_all_month, name='stats_all_month'),

    # 전체 주간 통계 "{% url 'posture:stats_all_week' %}"
    path('stats_all_week/', views.stats_all_week, name='stats_all_week'),

    # 전체 일별 통계 "{% url 'posture:stats_all_day' %}"
    path('stats_all_day/', views.stats_all_day, name='stats_all_day'),

    # 거북목 월간통계 "{% url 'posture:stats_turtle_month' %}"
    path('stats_turtle_month/', views.stats_turtle_month, name='stats_turtle_month'),

    # 거북목 주간통계 "{% url 'posture:stats_turtle_week' %}"
    path('stats_turtle_week/', views.stats_turtle_week, name='stats_turtle_week'),

    # 거북목 일간통계 "{% url 'posture:stats_turtle_day' %}"
    path('stats_turtle_day/', views.stats_turtle_day, name='stats_turtle_day'),

    # 어깨비대칭 월간통계 "{% url 'posture:stats_shoulder_month' %}"
    path('stats_shoulder_month/', views.stats_shoulder_month, name='stats_shoulder_month'),

    # 어깨비대칭 주간통계 "{% url 'posture:stats_shoulder_week' %}"
    path('stats_shoulder_week/', views.stats_shoulder_week, name='stats_shoulder_week'),

    # 어깨비대칭 일별통계 "{% url 'posture:stats_shoulder_day' %}"
    path('stats_shoulder_day/', views.stats_shoulder_day, name='stats_shoulder_day'),

    # 턱괴기 월간통계 "{% url 'posture:stats_jaw_month' %}"
    path('stats_jaw_month/', views.stats_jaw_month, name='stats_jaw_month'),

    # 턱괴기 주간통계 "{% url 'posture:stats_jaw_week' %}"
    path('stats_jaw_week/', views.stats_jaw_week, name='stats_jaw_week'),

    # 턱괴기 일별통계 "{% url 'posture:stats_jaw_day' %}"
    path('stats_jaw_day/', views.stats_jaw_day, name='stats_jaw_day'),
    
]