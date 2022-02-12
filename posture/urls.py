from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='main'), # 메인페이지
]