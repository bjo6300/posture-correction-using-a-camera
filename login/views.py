from django.shortcuts import render, get_object_or_404, redirect

def login(request):
    """ 로그인 메인 """
    return render(request, 'login/login.html')
