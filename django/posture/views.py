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

# 회원가입
def signup(request):
    return render(request, 'navbar/signup.html')

# 전체 월간 통계
def stats_all_month(request):
    return render(request, 'navbar/statistics/stats_all_month.html')

# 거북목 월간 통계
def stats_turtle_month(request):
    return render(request, 'navbar/statistics/stats_turtle_month.html')

# 거북목 주간 통계
def stats_turtle_week(request):
    return render(request, 'navbar/statistics/stats_turtle_week.html')

# 거북목 일간 통계
def stats_turtle_day(request):
    return render(request, 'navbar/statistics/stats_turtle_day.html')

# 어깨비대칭 월간 통계
def stats_shoulder_month(request):
    return render(request, 'navbar/statistics/stats_shoulder_month.html')

# 턱괴기 월간 통계
def stats_jaw_month(request):
    return render(request, 'navbar/statistics/stats_jaw_month.html')
