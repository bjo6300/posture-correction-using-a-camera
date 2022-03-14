from django.shortcuts import render
from django.http import HttpResponse
from common import views

app_name = 'common'

# 아이디찾기
def find_id(request):
    return render(request, 'common/find_id.html')

# 아이디찾기 체크완료
def find_id_checked(request):
    return render(request, 'common/find_id_checked.html')
