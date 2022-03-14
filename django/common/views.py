from django.shortcuts import render
from django.http import HttpResponse
from common import views

app_name = 'common'

# 회원가입
def find_id(request):
    return render(request, 'common/find_id.html')
