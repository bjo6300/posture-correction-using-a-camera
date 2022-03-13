from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # 홈 화면
    return render(request, 'main.html')

# 마이페이지
def mypage(request):
    return render(request, 'navbar/mypage/mypage.html')

# 마이페이지 수정하기
def mypage_modify(request):
    return render(request, 'navbar/mypage/mypage_modify.html')