from django.http import HttpResponse
from common import views
from django.contrib import auth, messages
from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth.forms import PasswordChangeForm # 비밀번호 변경 폼
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash # 비밀번호 변경 후 자동로그인
import ctypes
from django.views import View

app_name = 'common'

# 로그인 함수
def login_main(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password) # 여기서 username, password는 고정 (django 특)
        
        if user is None:
            return render(request, 'common/login.html', {'error': '아이디 또는 비밀번호를 확인해주세요.'})
        else:
            auth.login(request, user)
            return redirect('/home/')
    elif request.method == 'GET':
        return render(request, 'common/login.html')

# 회원가입 클래스
class SignUpView(View):
    # POST 요청 시
    def post(self, request):
        username = request.POST.get('username', None)  # 아이디
        password1 = request.POST.get('password1', None)  # 비밀번호
        password2 = request.POST.get('password2', None)  # 비밀번호(확인)
        email = request.POST.get('email', None)  # 이메일
        birth = request.POST.get('birth', None)  # 생일
        gender = request.POST.get('gender', None) # 성별
        
        # 아이디가 5자 미만이면
        if len(username) < 5:
            messages.warning(request, '아이디를 5글자 이상 입력해주세요.')
            return render(request, 'navbar/signup.html')

        # 아이디 중복 확인
        elif User.objects.filter(username=username).exists():  # 아이디 중복 체크
            messages.warning(request, '이미 존재하는 아이디입니다!')
            return redirect('/common/signup/')

        # 비밀번호 일치 여부 확인
        elif password1 != password2:
            messages.warning(request, '비밀번호가 일치하지 않습니다.')
            return render(request, 'navbar/signup.html')

        # # 이메일 형식 확인
        # elif email.find('@') | email.find('.') == -1:
        #     messages.warning(request, '올바른 이메일 형식을 입력해주세요.')
        #     return render(request, 'navbar/signup.html')

        # 빈 칸 확인
        if not (username and gender and password1 and password2 and email and birth):
            messages.warning(request, '사용 가능한 아이디입니다. 나머지 정보를 입력해주세요.')
            return render(request, 'navbar/signup.html')

        # DB에 사용자 계정 생성
        user = User.objects.create_user(username=username, gender=gender,
                                        email=email, birth=birth,
                                        password=password1)
        user.save()
        return render(request, 'navbar/signup_completed.html')

    # GET 요청 시(회원가입 버튼 클릭 등)
    def get(self, request):
        return render(request, 'navbar/signup.html')


def signup_completed(request):
    """ 회원가입 완료 페이지 """
    return render(request, 'navbar/signup_completed.html')

from .forms import CustomPasswordChangeForm, CustomEmailChangeForm

# 비밀번호 수정
def change_password(request):
    if request.method == 'POST':
        print('비밀번호 변경 POST')
        password_change_form = CustomPasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, " ")
            return render(request, 'navbar/mypage/modify_password_completed.html')
        else: # 사용자가 기존비밀번호를 제대로 입력 안했을 때
            # messages.error(request, "기존 비밀번호가 일치하지 않습니다.")
            return render(request, "navbar/mypage/change_password.html",{'form': password_change_form})
    elif request.method == 'GET':
        print('비밀번호 변경 GET')
        password_change_form = CustomPasswordChangeForm(request.user)
        return render(request, "navbar/mypage/change_password.html", {'form': password_change_form})

# 비밀번호 수정 완료
def modify_password_completed(request):
    return render(request, 'navbar/mypage/modify_password_completed.html') 

# 이메일 수정
def modify_email(request):
    if request.method == 'POST':
        # print('이메일 변경 POST')
        form = CustomEmailChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            # messages.success(request, "success ")
            return render(request, 'navbar/mypage/modify_email_completed.html')
        else:
            # messages.error(request, "fail")
            return render(request, "navbar/mypage/modify_email.html",{'form': form})
    elif request.method == 'GET':
        # print('이메일 변경 GET')
        form = CustomEmailChangeForm(instance=request.user)
    
    return render(request, "navbar/mypage/modify_email.html", {'form': form})

# 이메일 수정 완료
def modify_email_completed(request):
    return render(request, 'navbar/mypage/modify_email_completed.html') 


# from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# 아이디찾기
def find_id(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.Objects.get(email=email)
            if user.exists():
                template = render_to_string('common/send_email.html', {'name': user.username})
                method_email = EmailMessage(
                    'Your ID is in the email',
                    template,
                    to=[email]
                )
                method_email.send(fail_silently=False)
                return render(request, 'common/find_id_checked.html')
        except:
            messages.info(request, "There is no username along with the email")

    elif request.method == 'GET':
        return render(request, 'common/find_id.html')
    return render(request, 'common/find_id.html')


    # if request.method == 'POST':
    #     target_username = request.data.get('username', '')
    #     target_email = request.data.get('email', '')
    #
    #     target_user = User.objects.filter(
    #         username = target_username, email = target_email
    #     )
    #
    #     if target_user.exists():
    #         auth_string = email_auth_string()
    #         target_user.first().profile.auth = auth_string
    #         target_user.first().profile.save()
    #
    #         mail_title = '아이디 찾기 인증 메일입니다.'
    #         message = render_to_string('send_email_id.html', {'name': 'User.username'}, {'auth_string'})
    #         mail_to = 'User.email'
    #         email = EmailMessage(mail_title, message, to=[mail_to])
    #         email.send()
    #         return render(request, 'common/find_id.html')
            # try:
            # mail_title = '아이디 찾기 인증 메일입니다.'
            # message = render_to_string('send_email_id.html', {'name': 'User.username'}, {'auth_string'})
            # mail_to = 'User.email'
            # email = EmailMessage(mail_title, message, to=[mail_to])                email.send()
            # return render(request, 'common/find_id.html')

            # except:
            #     return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #     else:
    #         return render(request, 'common/find_id.html')
    # elif request.method == 'GET':
    #     return render(request, 'common/find_id.html')
    # return render(request, 'common/find_id.html')

        # 아이디찾기 체크완료
def find_id_checked(request):
    return render(request, 'common/find_id_checked.html')
