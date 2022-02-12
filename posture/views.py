from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # 홈 화면
    return render(request, 'main.html')