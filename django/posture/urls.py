from unicodedata import name
from django.urls import path

from . import views

app_name = 'posture'


urlpatterns = [
    # 메인페이지 "{% url 'posture:main' %}"
    path('', views.index, name='main'), 

    # 마이페이지 "{% url 'posture:mypage' %}"
    path('mypage/', views.mypage, name='mypage'),

    
]