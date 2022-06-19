from django.shortcuts import render
from django.http import HttpResponse
from .models import correction_video

def index(request):
    # 홈 화면
    return render(request, 'main.html')

# 메인페이지 - 프로그램 시작
def program(request):
    return render(request, 'program.html')

# 거북목 추천 영상
def recommended_turtle(request):
    video = correction_video.objects.filter(posture='거북목').order_by('video_index')

    return render(request, 'navbar/recommended/recommended_turtle.html',{'correction_video' : video})

# 거북목 추천 영상 보여주기
def show_turtle_videos(request):
    return render(request, 'navbar/recommended/show_turtle_videos.html')

# 어꺠비대칭 추천 영상
def recommended_shoulder(request):
    return render(request, 'navbar/recommended/recommended_shoulder.html')

# 턱괴기 추천 영상
def recommended_jaw(request):
    return render(request, 'navbar/recommended/recommended_jaw.html')

# 마이페이지
def mypage(request):
    return render(request, 'navbar/mypage/mypage.html')

# 마이페이지 수정하기
def mypage_modify(request):
    return render(request, 'navbar/mypage/mypage_modify.html')

# 전체 월간 통계
def stats_all_month(request):
    return render(request, 'navbar/statistics/stats_all_month.html')

# 전체 주간 통계
def stats_all_week(request):
    return render(request, 'navbar/statistics/stats_all_week.html')

# 전체 일별 통계
def stats_all_day(request):
    return render(request, 'navbar/statistics/stats_all_day.html')

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

# 어깨비대칭 주간 통계
def stats_shoulder_week(request):
    return render(request, 'navbar/statistics/stats_shoulder_week.html')

# 어깨비대칭 일별 통계
def stats_shoulder_day(request):
    return render(request, 'navbar/statistics/stats_shoulder_day.html')

# 턱괴기 월간 통계
def stats_jaw_month(request):
    return render(request, 'navbar/statistics/stats_jaw_month.html')

# 턱괴기 주간 통계
def stats_jaw_week(request):
    return render(request, 'navbar/statistics/stats_jaw_week.html')

# 턱괴기 일별 통계
def stats_jaw_day(request):
    return render(request, 'navbar/statistics/stats_jaw_day.html')
