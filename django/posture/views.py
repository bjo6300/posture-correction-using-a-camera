import json

from django.shortcuts import render
from django.db import connection
from datetime import datetime
from django.contrib.auth.models import User
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
    video = correction_video.objects.filter(posture='어깨비대칭').order_by('video_index')
    return render(request, 'navbar/recommended/recommended_shoulder.html',{'correction_video' : video})

# 턱괴기 추천 영상
def recommended_jaw(request):
    video = correction_video.objects.filter(posture='턱 괴기').order_by('video_index')
    return render(request, 'navbar/recommended/recommended_jaw.html',{'correction_video' : video})

# 마이페이지
def mypage(request):
    return render(request, 'navbar/mypage/mypage.html')

# 마이페이지 수정하기
def mypage_modify(request):
    return render(request, 'navbar/mypage/mypage_modify.html')

# 전체 월간 통계
def stats_all_month(request):
    cursor = connection.cursor();

    strSql = "select posturename, count(posturename) from common_posturelog where username='" + request.session.get(
        'username') + "' and date between date_add(NOW(), interval - 30 day) and NOW() " \
                      "GROUP By posturename"

    result = cursor.execute(strSql)
    datas = cursor.fetchall()

    connection.close()

    data_dict = {0: 0, 1: 0, 2: 0}
    for type, data in datas:
        data_dict[type] = data

    return render(request, 'navbar/statistics/stats_all_month.html', {'datas': json.dumps(data_dict)})

# 전체 주간 통계
def stats_all_week(request):
    cursor = connection.cursor();

    strSql = "select posturename, count(posturename) from common_posturelog where username='" + request.session.get(
        'username') + "' and date between date_add(NOW(), interval - 7 day) and NOW() " \
                      "GROUP By posturename"

    result = cursor.execute(strSql)
    datas = cursor.fetchall()

    connection.close()

    data_dict = {0: 0, 1: 0, 2: 0}
    for type, data in datas:
        data_dict[type] = data

    return render(request, 'navbar/statistics/stats_all_week.html', {'datas': json.dumps(data_dict)})

# 전체 일별 통계
def stats_all_day(request):
    cursor = connection.cursor();

    strSql = "select posturename, count(posturename) from common_posturelog where username='" + request.session.get(
        'username') + "' and date between date_format(now(), '%Y-%m-%d 00:00:00') and date_format(now(), '%Y-%m-%d 23:59:59') " \
                      "GROUP By posturename"

    result = cursor.execute(strSql)
    datas = cursor.fetchall()

    connection.close()

    data_dict = {0: 0,1: 0,2: 0}
    for type, data in datas:
        data_dict[type] = data

    return render(request, 'navbar/statistics/stats_all_day.html', {'datas': json.dumps(data_dict)})

# 거북목 월간 통계
def stats_turtle_month(request):
    cursor = connection.cursor();

    strSql = "select month(date) AS mm, COUNT(date) as cnt from common_posturelog where date " \
             "between date_add(NOW(), interval - 365 day) and NOW() and username='" + request.session.get(
        'username') + "' and posturename = 2 GROUP By mm order by mm asc"

    result = cursor.execute(strSql)
    datas = cursor.fetchall()

    strSql2 = "select month(Now())"
    result2 = cursor.execute(strSql2)
    data2 = cursor.fetchall()

    connection.close()

    # data dict 초기화
    # 1~7 일~토
    data_dict = {}
    for i in range(0, 25):
        data_dict[i] = 0

    data_dict[0] = int(data2[0][0])  # 현재 월 출력
    for hour, data in datas:
        data_dict[hour] = data
        data_dict[hour + 12] = data

    return render(request, 'navbar/statistics/stats_turtle_month.html', {'datas': json.dumps(data_dict)})

# 거북목 주간 통계
def stats_turtle_week(request):
    cursor = connection.cursor();

    strSql = "select dayofweek(date) AS dw, COUNT(date) as cnt from common_posturelog where date " \
             "between date_add(NOW(), interval - 30 day) and NOW() and username='" + request.session.get(
        'username') + "' and posturename = 2 GROUP By dw order by dw asc"

    result = cursor.execute(strSql)
    datas = cursor.fetchall()

    strSql2 = "select dayofweek(Now())"
    result2 = cursor.execute(strSql2)
    data2 = cursor.fetchall()

    connection.close()

    # data dict 초기화
    # 1~7 일~토
    data_dict = {}
    for i in range(0, 15):
        data_dict[i] = 0

    data_dict[0] = int(data2[0][0])  # 현재 요일 출력
    for hour, data in datas:
        data_dict[hour] = data
        data_dict[hour + 7] = data

    return render(request, 'navbar/statistics/stats_turtle_week.html', {'datas': json.dumps(data_dict)})

# 거북목 일간 통계
def stats_turtle_day(request):
    cursor = connection.cursor();

    strSql = "select HOUR(date) AS hh, COUNT(date) as cnt from common_posturelog where date " \
             "between date_format(now(), '%Y-%m-%d 00:00:00') and date_format(now(), '%Y-%m-%d 23:59:59') and username='" + request.session.get(
        'username') + "' and posturename = 2 GROUP By hh order by hh asc"

    result = cursor.execute(strSql)
    datas = cursor.fetchall()

    connection.close()

    # data dict 초기화
    data_dict = {}
    for i in range(24):
        data_dict[i] = 0

    for hour, data in datas:
        data_dict[hour] = data

    return render(request, 'navbar/statistics/stats_turtle_day.html', {'datas': json.dumps(data_dict)})

# 어깨비대칭 월간 통계
def stats_shoulder_month(request):
    cursor = connection.cursor();

    strSql = "select month(date) AS mm, COUNT(date) as cnt from common_posturelog where date " \
             "between date_add(NOW(), interval - 365 day) and NOW() and username='" + request.session.get(
        'username') + "' and posturename = 1 GROUP By mm order by mm asc"

    result = cursor.execute(strSql)
    datas = cursor.fetchall()

    strSql2 = "select month(Now())"
    result2 = cursor.execute(strSql2)
    data2 = cursor.fetchall()

    connection.close()

    # data dict 초기화
    # 1~7 일~토
    data_dict = {}
    for i in range(0, 25):
        data_dict[i] = 0

    data_dict[0] = int(data2[0][0])  # 현재 월 출력
    for hour, data in datas:
        data_dict[hour] = data
        data_dict[hour + 12] = data

    return render(request, 'navbar/statistics/stats_shoulder_month.html', {'datas': json.dumps(data_dict)})

# 어깨비대칭 주간 통계
def stats_shoulder_week(request):
    cursor = connection.cursor();

    strSql = "select dayofweek(date) AS dw, COUNT(date) as cnt from common_posturelog where date " \
             "between date_add(NOW(), interval - 30 day) and NOW() and username='" + request.session.get(
        'username') + "' and posturename = 1 GROUP By dw order by dw asc"

    result = cursor.execute(strSql)
    datas = cursor.fetchall()

    strSql2 = "select dayofweek(Now())"
    result2 = cursor.execute(strSql2)
    data2 = cursor.fetchall()

    connection.close()

    # data dict 초기화
    # 1~7 일~토
    data_dict = {}
    for i in range(0, 15):
        data_dict[i] = 0

    data_dict[0] = int(data2[0][0])  # 현재 요일 출력
    for hour, data in datas:
        data_dict[hour] = data
        data_dict[hour + 7] = data

    return render(request, 'navbar/statistics/stats_shoulder_week.html', {'datas': json.dumps(data_dict)})

# 어깨비대칭 일별 통계
def stats_shoulder_day(request):
    cursor = connection.cursor();

    strSql = "select HOUR(date) AS hh, COUNT(date) as cnt from common_posturelog where date " \
             "between date_format(now(), '%Y-%m-%d 00:00:00') and date_format(now(), '%Y-%m-%d 23:59:59') and username='" + request.session.get(
        'username') + "' and posturename = 1 GROUP By hh order by hh asc"

    result = cursor.execute(strSql)
    datas = cursor.fetchall()

    connection.close()

    # data dict 초기화
    data_dict = {}
    for i in range(24):
        data_dict[i] = 0

    for hour, data in datas:
        data_dict[hour] = data

    return render(request, 'navbar/statistics/stats_shoulder_day.html', {'datas': json.dumps(data_dict)})

# 턱괴기 월간 통계
def stats_jaw_month(request):
    cursor = connection.cursor();

    strSql = "select month(date) AS mm, COUNT(date) as cnt from common_posturelog where date " \
             "between date_add(NOW(), interval - 365 day) and NOW() and username='" + request.session.get(
        'username') + "' and posturename = 0 GROUP By mm order by mm asc"

    result = cursor.execute(strSql)
    datas = cursor.fetchall()

    strSql2 = "select month(Now())"
    result2 = cursor.execute(strSql2)
    data2 = cursor.fetchall()

    connection.close()

    # data dict 초기화
    # 1~7 일~토
    data_dict = {}
    for i in range(0, 25):
        data_dict[i] = 0

    data_dict[0] = int(data2[0][0])  # 현재 월 출력
    for hour, data in datas:
        data_dict[hour] = data
        data_dict[hour + 12] = data

    return render(request, 'navbar/statistics/stats_jaw_month.html', {'datas': json.dumps(data_dict)})

# 턱괴기 주간 통계
def stats_jaw_week(request):
    cursor = connection.cursor();

    strSql = "select dayofweek(date) AS dw, COUNT(date) as cnt from common_posturelog where date " \
             "between date_add(NOW(), interval - 30 day) and NOW() and username='" + request.session.get(
        'username') + "' and posturename = 0 GROUP By dw order by dw asc"

    result = cursor.execute(strSql)
    datas = cursor.fetchall()

    strSql2 = "select dayofweek(Now())"
    result2 = cursor.execute(strSql2)
    data2 = cursor.fetchall()

    connection.close()

    # data dict 초기화
    # 1~7 일~토
    data_dict = {}
    for i in range(0,15):
        data_dict[i] = 0

    data_dict[0] = int(data2[0][0])   # 현재 요일 출력
    for hour, data in datas:
        data_dict[hour] = data
        data_dict[hour+7] = data

    return render(request, 'navbar/statistics/stats_jaw_week.html', {'datas': json.dumps(data_dict)})

# 턱괴기 일별 통계
def stats_jaw_day(request):
    cursor = connection.cursor();

    strSql = "select HOUR(date) AS hh, COUNT(date) as cnt from common_posturelog where date " \
             "between date_format(now(), '%Y-%m-%d 00:00:00') and date_format(now(), '%Y-%m-%d 23:59:59') and username='" + request.session.get(
        'username') + "' and posturename = 0 GROUP By hh order by hh asc"

    result = cursor.execute(strSql)
    datas = cursor.fetchall()

    connection.close()

    # data dict 초기화
    data_dict = {}
    for i in range(24):
        data_dict[i] = 0

    for hour, data in datas:
        data_dict[hour] = data

    return render(request, 'navbar/statistics/stats_jaw_day.html', {'datas': json.dumps(data_dict)})
