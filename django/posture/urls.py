from unicodedata import name
from django.urls import path

from . import views

app_name = 'posture'


urlpatterns = [
    path('', views.index, name='main'), # 메인페이지 "{% url 'posture:main' %}"
]