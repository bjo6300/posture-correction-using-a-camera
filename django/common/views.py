from django.http import HttpResponse
from common import views
from django.contrib import auth, messages
from django.shortcuts import render, redirect
from .models import User

import ctypes
from django.views import View

app_name = 'common'

# 로그인 함수
def login_main(request):
    if request.method == 'POST':
        user_id = request.POST['username']
        user_password = request.POST['password']
        user = auth.authenticate(request, username=user_id, password=user_password) # 여기서 username, password는 고정 (django 특)
        
        if user is None:
            return render(request, 'common/login.html', {'error': 'user_id or password가 틀렸습니다.'})
        else:
            auth.login(request, user)
            return redirect('/home/')
    elif request.method == 'GET':
        return render(request, 'common/login.html')

# 회원가입 클래스
class SignUpView(View):
    # POST 요청 시
    def post(self, request):
        user_id = request.POST.get('user_id', None)  # 아이디
        password1 = request.POST.get('password1', None)  # 비밀번호
        password2 = request.POST.get('password2', None)  # 비밀번호(확인)
        user_email = request.POST.get('user_email', None)  # 이메일
        birth = request.POST.get('birth', None)  # 생일
        gender = request.POST.get('gender', None) # 성별
        
        res_data = {}

        # 빈 칸 확인
        if not (user_id and user_id and password1 and password2 and user_email and birth):
            res_data['error'] = "입력하지 않은 칸이 있습니다."

        # 아이디가 5자 미만이면
        if len(user_id) < 5:
            messages.warning(request, '아이디를 5글자 이상 입력해주세요.')
            return render(request, 'navbar/signup.html')

        # 아이디 중복 확인
        if User.objects.filter(user_id=user_id).exists():  # 아이디 중복 체크
            messages.warning(request, '이미 존재하는 아이디입니다!')
            return render(request, 'navbar/signup.html')

        # 비밀번호 일치 여부 확인
        if password1 != password2:
            res_data['error'] = '비밀번호가 일치하지 않습니다.'

        # DB에 사용자 계정 생성
        user = User.objects.create_user(user_id=user_id, gender=gender,
                                        user_email=user_email, birth=birth,
                                        user_password=password1)
        user.save()
        return render(request, 'navbar/signup_completed.html', res_data)

    # GET 요청 시(회원가입 버튼 클릭 등)
    def get(self, request):
        return render(request, 'navbar/signup.html')

def signup_completed(request):
    """ 회원가입 완료 페이지 """
    return render(request, 'navbar/signup_completed.html')


# 아이디찾기
def find_id(request):
    return render(request, 'common/find_id.html')

# 아이디찾기 체크완료
def find_id_checked(request):
    return render(request, 'common/find_id_checked.html')
