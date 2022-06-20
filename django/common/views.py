from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib import messages
from .forms import CustomPasswordChangeForm, CustomEmailChangeForm, PostureLogForm
import cv2
import threading
from django.shortcuts import render
import numpy as np
from django.http.response import JsonResponse, HttpResponse
from django.http import StreamingHttpResponse
import time
from common.modules import HolisticModule as hm
from win10toast import ToastNotifier
import tensorflow as tf
from keras.models import load_model
from keras.utils import np_utils
from keras.models import Sequential
from keras.preprocessing.image import img_to_array
from PIL import Image
from django.http import HttpResponse
from common import views
from django.contrib import auth, messages
from django.shortcuts import render, redirect
from .models import User, PostureLog
from django.contrib.auth.forms import PasswordChangeForm  # 비밀번호 변경 폼
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash  # 비밀번호 변경 후 자동로그인
import ctypes
from django.views import View

# fps = 1초당 프레임의 수
# privious time for fps
pTime = 0
# cerrent time for fps
cTime = 0

# 모델 불러오기
model = tf.keras.models.load_model('common\\saved_model')

# Holistic 객체(어떠한 행위를 하는 친구) 생성
detector = hm.HolisticDetector()

# toast 알림을 주는 객체 생성
toaster = ToastNotifier()

# 턱 괴기 변수 초기 세팅
jaw_bone_count = 0

# 턱 괴기 교정 카운트 변수 초기 세팅
p_jaw_bone_count = 0

# 실제 턱 괴기 변수 초기 세팅
real_jaw_bone_count = 0

# 어깨 비대칭 변수 초기 세팅
shoulder_count = 0

# 어깨 비대칭 교정 카운트 변수 초기 세팅
p_shoulder_count = 0

# 실제 어깨 비대칭 변수 초기 세팅
real_shoulder_count = 0

# 양 어깨 높이 차이 변수
shoulder_hd = 0

# 거북목 변수 초기 세팅
turtleNeck_count = 0

# 거북목 교정 카운트 변수 초기 세팅
p_turtleNeck_count = 0

# 실제 거북목 변수 초기 세팅
real_turtleNeck_count = 0

# postureLog 객체 생성
postureLog = PostureLog()

app_name = 'common'


class VideoCamera(object):
    # capture mode
    mode = 2

    # stretching value
    isStretchingPose = False

    # 방향 위치 : 0(오른쪽), 1(왼쪽)
    currentDirection = 0

    # 방향 위치 : 0(위), 1(아래)
    upDown = 0

    # username
    usrname = ''

    # 입 동작 : 0(아), 1(이)
    mouth_mode = 0

    # 교정 횟수
    stretching_count = 0

    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    # If you decide to use video.mp4, you must have this file in the folder
    # as the main.py.
    # self.video = cv2.VideoCapture('video.mp4')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        # default BGR img

        # Holistic detector을 이용한 감지
        frame = detector.findHolistic(self.frame, draw=True)

        # output -> list ( id, x, y, z) 32 개 좌표인데 예를 들면, (11, x, y, z)
        pose_lmList = detector.findPoseLandmark(frame, draw=True)
        # 468개의 얼굴 점 리스트
        face_lmList = detector.findFaceLandmark(frame, draw=True)

        # fps 계산 로직
        cTime = time.time()
        global pTime
        fps = 1 / (cTime - pTime)
        pTime = cTime

        # 사용자의 컴퓨터에 맞는 주사율
        my_computer_fps = fps + 1

        # 웹캠 이미지 저장
        turtleNeck_frame = cv2.imwrite('frame.jpg', frame)

        # 이미지 파일 경로

        file_link = "frame.jpg"

        # 인체가 감지가 되었는지 확인하는 구문
        if len(pose_lmList) != 0 and len(face_lmList) != 0:

            # 이미지 RGB 변환 및 사이즈 조정
            img = Image.open(file_link)
            img = img.convert("RGB")
            img = img.resize((64, 64))

            # 이미지 배열화 및 차원 확장
            turtleNeck_region = img_to_array(img)
            turtleNeck_region = np.expand_dims(turtleNeck_region, axis=0)

            single_test = model.predict(turtleNeck_region)

            # Holistic_module에 있는 findDistance의 p2값을 수정하여 사용
            # 왼쪽 center_left_hand 좌표와 얼굴 152번(턱) 좌표를 사용하여 길이를 구하는 부분

            # 양쪽 손 관절점 위치를 찾는 함수
            left_hand_len = detector.findPointDistance(152, 20)
            right_hand_len = detector.findPointDistance(152, 17)

            # 양 어깨의 관절점 사이의 거리를 이미지로 변경
            shoulder_img = detector.drawShoulder(11, 12, frame, draw=True)

            # 어깨의 y값 비교하여 양 쪽 어깨의 높이가 다르면 어깨 비대칭으로 인식
            shoulder_hd = detector.findShoulder(11, 12)

            # 양쪽 손 관절점 위치를 시각화 하는 함수
            left_hand_img = detector.drawPointDistance(
                152, 20, frame, draw=True)
            right_hand_img = detector.drawPointDistance(
                152, 17, frame, draw=True)

            mouth_img = detector.drawMouth(frame, draw=True)

            mouth_img = detector.drawMouth(frame, draw=True)

            global jaw_bone_count
            global p_jaw_bone_count
            global real_jaw_bone_count
            global shoulder_count
            global p_shoulder_count
            global real_shoulder_count
            global turtleNeck_count
            global p_turtleNeck_count
            global real_turtleNeck_count

            # 턱 괴기 자세가 감지되면 턱 괴기 count 1증가
            if left_hand_len < 130 or right_hand_len < 130:
                jaw_bone_count += 1
                shoulder_count = 0
                turtleNeck_count = 0
            elif left_hand_len < 25 or right_hand_len < 25:
                jaw_bone_count = 0
            else:
                jaw_bone_count = 0

            # 어깨 비대칭 자세가 감지되면 어깨 비대칭 count 1증가
            if shoulder_hd >= 30:
                shoulder_count += 1
            else:
                shoulder_count = 0

            # 거북목이 감지되면 count가 1증가
            if single_test == 1:
                turtleNeck_count += 1
            else:
                turtleNeck_count = 0

            # 3초동안 턱 괴기 자세가 인식되면 알림을 제공한다.
            if jaw_bone_count > my_computer_fps * 3:
                # 자세 인식 후, insert DB
                self.insertLog(self.usrname, 0)

                print("턱괴기 자세가 감지되었습니다!")

                # win10toast 알림 제
                toaster.show_toast(
                    "턱 괴기 발생!", f"바른 자세를 취해주세요!.\n\n", threaded=True)

                # 알림 제공 후 카운트를 다시 0으로 만든다.
                jaw_bone_count = 0
                p_jaw_bone_count += 1
                real_jaw_bone_count += 1

            if shoulder_count > my_computer_fps * 3:
                # 자세 인식 후, insert DB
                self.insertLog(self.usrname, 1)

                print("어깨 비대칭 동작이 감지되었습니다!")

                toaster.show_toast(
                    "어깨 비대칭 발생!", f"바른 자세를 취해주세요!", threaded=True)

                # 알림 제공 후 카운트를 다시 0으로 만듬
                shoulder_count = 0
                p_shoulder_count += 1
                real_shoulder_count += 1

            if turtleNeck_count > my_computer_fps * 3:
                # 자세 인식 후, insert DB
                self.insertLog(self.usrname, 2)

                print("거북목 동작이 감지되었습니다!")
                # win10toast 알림 제공
                toaster.show_toast(
                    "거북목 발생!", f"바른 자세를 취해주세요!.\n\n", threaded=True)

                # 알림 제공 후 카운트를 다시 0으로 만든다.
                turtleNeck_count = 0
                p_turtleNeck_count += 1
                real_turtleNeck_count += 1

            if p_shoulder_count != 0 and p_shoulder_count % 3 == 0:
                VideoCamera.mode = 1
            elif p_turtleNeck_count != 0 and p_turtleNeck_count % 3 == 0:
                VideoCamera.mode = 2
            elif p_jaw_bone_count != 0 and p_jaw_bone_count % 3 == 0:
                VideoCamera.mode = 3

        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def get_frame_stretching(self):

        global p_jaw_bone_count
        global p_shoulder_count
        global p_turtleNeck_count
        # default BGR img

        # Holistic detector을 이용한 감지
        frame = detector.findHolistic(self.frame, draw=True)

        # output -> list ( id, x, y, z) 32 개 좌표인데 예를 들면, (11, x, y, z)
        pose_lmList = detector.findPoseLandmark(frame, draw=True)
        # 468개의 얼굴 점 리스트
        face_lmList = detector.findFaceLandmark(frame, draw=True)

        # fps 계산 로직
        cTime = time.time()
        global pTime
        fps = 1 / (cTime - pTime)
        pTime = cTime

        # 사용자의 컴퓨터에 맞는 주사율
        my_computer_fps = fps + 1

        # 인체가 감지가 되었는지 확인하는 구문
        if len(pose_lmList) != 0 and len(face_lmList) != 0:

            # 양쪽 귀 관절점 사이의 거리를 이미지로 변경
            ears_img = detector.drawEars(frame, draw=True)

            # 양 어깨의 관절점 사이의 거리를 이미지로 변경
            shoulder_img = detector.drawShoulder2(frame, draw=True)

            # 양쪽 손과 눈썹 사이 거리 구하기
            left_hand_position = detector.findPointDistance2(21, 6)
            right_hand_position = detector.findPointDistance2(22, 3)
            # print(left_hand_position, right_hand_position)

            # 양쪽 귀의 기울기 값 계산
            ears_inclination = detector.findinclination(7, 8)

            if VideoCamera.isStretchingPose == True:  # 포즈가 취해졌는지 판단
                if VideoCamera.currentDirection == 0:  # 오른쪽
                    VideoCamera.currentDirection = 1  # 왼쪽
                    VideoCamera.isStretchingPose = False
                else:  # 왼쪽
                    VideoCamera.mode = 0
                    VideoCamera.isStretchingPose = False
                    VideoCamera.currentDirection = 0
            else:
                if VideoCamera.currentDirection == 0:  # 오른쪽
                    toaster.show_toast(
                        "스트레칭 시작합니다.", f"오른손으로 반대편 머리를 감싼 후, 지긋이 오른쪽으로 눌러주세요!.\n\n", threaded=True)
                    # if ears_inclination <= -0.4:
                    if (ears_inclination <= -0.4) and (right_hand_position >= 0) and (right_hand_position <= 145):
                        VideoCamera.isStretchingPose = True
                else:  # 왼쪽
                    toaster.show_toast(
                        "스트레칭 시작합니다.", f"왼손으로 반대편 머리를 감싼 후, 지긋이 왼쪽으로 눌러주세요!.\n\n", threaded=True)
                    # if ears_inclination >= 0.4:
                    if (ears_inclination >= 0.4) and (left_hand_position >= 0) and (left_hand_position <= 145):
                        VideoCamera.isStretchingPose = True
                        p_shoulder_count = 0

        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def get_frame_stretching2(self):
        global p_jaw_bone_count
        global p_shoulder_count
        global p_turtleNeck_count
        # default BGR img

        # Holistic detector을 이용한 감지
        frame = detector.findHolistic(self.frame, draw=True)

        # output -> list ( id, x, y, z) 32 개 좌표인데 예를 들면, (11, x, y, z)
        pose_lmList = detector.findPoseLandmark(frame, draw=True)
        # 468개의 얼굴 점 리스트
        face_lmList = detector.findFaceLandmark(frame, draw=True)

        # fps 계산 로직
        cTime = time.time()
        global pTime
        fps = 1 / (cTime - pTime)
        pTime = cTime

        # 사용자의 컴퓨터에 맞는 주사율
        my_computer_fps = fps + 1

        # 인체가 감지가 되었는지 확인하는 구문
        if len(pose_lmList) != 0 and len(face_lmList) != 0:
            # 양쪽 귀 관절점 사이의 거리를 이미지로 변경
            ears_img = detector.drawEars(frame, draw=True)

            # 양 어깨의 관절점 사이의 거리를 이미지로 변경
            shoulder_img = detector.drawShoulder2(frame, draw=True)

            # 양쪽 손과 눈썹 사이 거리 구하기
            left_hand_position = detector.findPointDistance(10, 19)
            right_hand_position = detector.findPointDistance(10, 20)
            # print(left_hand_position, right_hand_position)

            # 턱 관절 각도 계산
            jaw_angle = detector.findAngle(frame, 150, 152, 365, draw=True)

            if VideoCamera.isStretchingPose == True:  # 포즈가 취해졌는지 판단
                if VideoCamera.upDown == 0:  # 위쪽
                    VideoCamera.upDown = 1  # 아래쪽
                    VideoCamera.isStretchingPose = False
                else:  # 아래쪽
                    VideoCamera.mode = 0
                    VideoCamera.isStretchingPose = False
                    VideoCamera.upDown = 0
            else:
                if VideoCamera.upDown == 0:  # 위쪽
                    toaster.show_toast(
                        "스트레칭 시작합니다.", f"양손 엄지손가락을 턱에 대고 턱을 위로 당겨주세요!\n\n", threaded=True)
                    # if jaw_angle >= 160:
                    if (jaw_angle >= 150) and (left_hand_position >= 100 and left_hand_position <= 200) and (right_hand_position >= 100 and right_hand_position <= 200):
                        VideoCamera.isStretchingPose = True
                else:  # 아래쪽
                    toaster.show_toast(
                        "스트레칭 시작합니다.", f"양손에 깍지를 끼고 머리를 아래로 당겨주세요!\n\n", threaded=True)
                    # print(left_hand_position)
                    # if jaw_angle <= 105:
                    if (jaw_angle <= 115) and (left_hand_position >= 50 and left_hand_position <= 120) \
                            and (right_hand_position >= 50 and right_hand_position <= 120):

                        VideoCamera.isStretchingPose = True
                        p_turtleNeck_count = 0

        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def get_frame_stretching3(self):
        global p_jaw_bone_count
        global p_shoulder_count
        global p_turtleNeck_count
        # default BGR img

        # Holistic detector을 이용한 감지
        frame = detector.findHolistic(self.frame, draw=True)

        # output -> list ( id, x, y, z) 32 개 좌표인데 예를 들면, (11, x, y, z)
        pose_lmList = detector.findPoseLandmark(frame, draw=True)
        # 468개의 얼굴 점 리스트
        face_lmList = detector.findFaceLandmark(frame, draw=True)

        # fps 계산 로직
        cTime = time.time()
        global pTime
        fps = 1 / (cTime - pTime)
        pTime = cTime

        # 사용자의 컴퓨터에 맞는 주사율
        my_computer_fps = fps + 1

        # 인체가 감지가 되었는지 확인하는 구문
        if len(pose_lmList) != 0 and len(face_lmList) != 0:
            # 양쪽 귀 관절점 사이의 거리를 이미지로 변경
            ears_img = detector.drawEars(frame, draw=True)

            # 양 어깨의 관절점 사이의 거리를 이미지로 변경
            shoulder_img = detector.drawShoulder2(frame, draw=True)

            # 양쪽 손과 눈썹 사이 거리 구하기
            left_hand_position = detector.findPointDistance(152, 19)
            right_hand_position = detector.findPointDistance(152, 20)
            # print(left_hand_position, right_hand_position)

            # 입 각도 계산
            mouth_distance1 = detector.findMouthDistance(frame, 0, 17)
            mouth_distance2 = detector.findMouthDistance(frame, 61, 291)

            mouth_angle = detector.findAngle(frame, 61, 17, 291)

            if VideoCamera.stretching_count == 3 and VideoCamera.mouth_mode == 1:
                VideoCamera.stretching_count = 0
                VideoCamera.mode = 0

            if VideoCamera.isStretchingPose == True:  # 포즈가 취해졌는지 판단
                if VideoCamera.mouth_mode == 0:
                    VideoCamera.mouth_mode = 1
                    VideoCamera.isStretchingPose = False
                else:
                    VideoCamera.isStretchingPose = False
                    VideoCamera.mouth_mode = 0
            else:
                if VideoCamera.mouth_mode == 0:
                    toaster.show_toast(
                        "스트레칭 시작합니다.", f"입을 아! 모양으로 크게 벌려주세요!\n\n", threaded=True)
                    # if jaw_angle >= 160:
                    if (mouth_angle >= 79 and mouth_angle <= 95) and mouth_distance1 >= 38:
                        VideoCamera.isStretchingPose = True
                else:
                    toaster.show_toast(
                        "스트레칭 시작합니다.", f"입을 이! 모양으로 크게 벌려주세요!\n\n", threaded=True)
                    # if jaw_angle >= 160:
                    if mouth_angle >= 113 and mouth_distance2 >= 60:
                        VideoCamera.isStretchingPose = True
                        p_jaw_bone_count = 0
                        VideoCamera.stretching_count += 1
            cv2.putText(frame, str(int(VideoCamera.stretching_count)),
                        (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

    # SQL insert
    def insertLog(self, username, postureType):
        postureLog = PostureLog(username=username, posturename=postureType)
        postureLog.save()
        return


cam = VideoCamera()


def gen(camera):
    while True:
        if VideoCamera.mode == 1:  # 스트레칭
            frame = cam.get_frame_stretching()
        elif VideoCamera.mode == 2:
            frame = cam.get_frame_stretching2()
        elif VideoCamera.mode == 3:
            frame = cam.get_frame_stretching3()
        else:  # 인식
            frame = cam.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def stream2(request):
    try:
        return StreamingHttpResponse(gen(()), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        pass

# 로그인 함수


def login_main(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # 여기서 username, password는 고정 (django 특)
        user = auth.authenticate(request, username=username, password=password)

        if user is None:
            return render(request, 'common/login.html', {'error': '아이디 또는 비밀번호를 확인해주세요.'})
        else:
            cam.usrname = username      # DB에 필요한 username 저장
            request.session['username'] = username  # session username 설정
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
        gender = request.POST.get('gender', None)  # 성별

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


# 비밀번호 수정
def change_password(request):
    if request.method == 'POST':
        print('비밀번호 변경 POST')
        password_change_form = CustomPasswordChangeForm(
            request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, " ")
            return render(request, 'navbar/mypage/modify_password_completed.html')
        else:  # 사용자가 기존비밀번호를 제대로 입력 안했을 때
            # messages.error(request, "기존 비밀번호가 일치하지 않습니다.")
            return render(request, "navbar/mypage/change_password.html", {'form': password_change_form})
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
            return render(request, "navbar/mypage/modify_email.html", {'form': form})
    elif request.method == 'GET':
        # print('이메일 변경 GET')
        form = CustomEmailChangeForm(instance=request.user)

    return render(request, "navbar/mypage/modify_email.html", {'form': form})

# 이메일 수정 완료


def modify_email_completed(request):
    return render(request, 'navbar/mypage/modify_email_completed.html')


# from django.conf import settings


# 아이디찾기
def find_id(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # print(user.email)
            template = render_to_string(
                'common/send_email.html', {'name': user.username})
            method_email = EmailMessage(
                '[PCP] PCP 아이디는 다음과 같습니다.',
                template,
                to=[email]
            )
            method_email.send(fail_silently=False)
            return render(request, 'common/find_id_checked.html')

        except:
            messages.info(request, "해당되는 이메일의 PCP 계정이 없습니다.")

    elif request.method == 'GET':
        return render(request, 'common/find_id.html')
    return render(request, 'common/find_id.html')

 # 아이디찾기 체크완료


def find_id_checked(request):
    return render(request, 'common/find_id_checked.html')
