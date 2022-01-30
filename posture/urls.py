from django.urls import path

from . import views

urlpatterns = [
    path('', views.index), # 메인페이지
]