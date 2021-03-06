import cv2
import time
import numpy as np
import pcp.modules.HolisticModule as hm
# from win10toast import ToastNotifier
import tensorflow as tf
from keras.preprocessing.image import img_to_array
from PIL import Image

# fps = 1초당 프레임의 수
# privious time for fps
pTime = 0
# cerrent time for fps
cTime = 0

# 모델 불러오기
model = tf.keras.models.load_model('saved_model')

# 웹캠 불러오기
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Holistic 객체(어떠한 행위를 하는 친구) 생성
detector = hm.HolisticDetector()

# toast 알림을 주는 객체 생성
toaster = ToastNotifier()

# 턱 괴기 변수 초기 세팅
jaw_bone_count = 0

# 실제 턱 괴기 변수 초기 세팅
real_jaw_bone_count = 0

# 어깨 비대칭 변수 초기 세팅
shoulder_count = 0

# 실제 어깨 비대칭 변수 초기 세팅
real_shoulder_count = 0

# 양 어깨 높이 차이 변수
shoulder_hd = 0

# 거북목 변수 초기 세팅
turtleNeck_count = 0

# 실제 거북목 변수 초기 세팅
real_turtleNeck_count = 0

while True:
    # default BGR img
    success, frame = cap.read()

    # Holistic detector을 이용한 감지
    frame = detector.findHolistic(frame, draw=True)

    # output -> list ( id, x, y, z) 32 개 좌표인데 예를 들면, (11, x, y, z)
    pose_lmList = detector.findPoseLandmark(frame, draw=True)
    # 468개의 얼굴 점 리스트
    face_lmList = detector.findFaceLandmark(frame, draw=True)

    # fps 계산 로직
    cTime = time.time()
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

        #
        single_test = model.predict(turtleNeck_region)

        # Holistic_module에 있는 findDistance의 p2값을 수정하여 사용
        # 왼쪽 center_left_hand 좌표와 얼굴 152번(턱) 좌표를 사용하여 길이를 구하는 부분

        # 양쪽 손 관절점 위치를 찾는 함수
        left_hand_len = detector.findPointDistance(152,20)
        right_hand_len = detector.findPointDistance(152, 17)

        # 양 어깨의 관절점 사이의 거리를 이미지로 변경
        shoulder_img = detector.drawShoulder(11,12,frame,draw=True)

        # 어깨의 y값 비교하여 양 쪽 어깨의 높이가 다르면 어깨 비대칭으로 인식
        shoulder_hd = detector.findShoulder(11, 12)

        # 양쪽 손 관절점 위치를 시각화 하는 함수
        left_hand_img = detector.drawPointDistance(152, 20, frame, draw=True)
        right_hand_img = detector.drawPointDistance(152, 17, frame, draw=True)

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
        if shoulder_hd >= 20:
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
            print("턱괴기 자세가 감지되었습니다!")
            # win10toast 알림 제공

            toaster.show_toast("턱 괴기 발생!", f"바른 자세를 취해주세요!.\n\n",threaded=True)

            # 알림 제공 후 카운트를 다시 0으로 만든다.
            jaw_bone_count = 0

            real_jaw_bone_count += 1

        if shoulder_count > my_computer_fps * 3:
            print("어깨 비대칭 동작이 감지되었습니다!")

            toaster.show_toast("어깨 비대칭 발생!",f"바른 자세를 취해주세요!",threaded=True)

            # 알림 제공 후 카운트를 다시 0으로 만듬
            shoulder_count = 0

            real_shoulder_count += 1

        if turtleNeck_count > my_computer_fps * 3:
            print("거북목 동작이 감지되었습니다!")
            # win10toast 알림 제공
            toaster.show_toast("거북목 발생!", f"바른 자세를 취해주세요!.\n\n",threaded=True)

            # 알림 제공 후 카운트를 다시 0으로 만든다.
            turtleNeck_count = 0

            turtleNeck_count += 1

        print("왼쪽 손 : {:.3f}, 오른쪽 손 : {:.3f}, 어깨 높이 차 : {:.1f}, 거북목 정확도 : {:.1f}".format(left_hand_len, right_hand_len, shoulder_hd, single_test[0][0]))


    # fps를 이미지 상단에 입력하는 로직
    cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    # img를 우리에게 보여주는 부분
    cv2.imshow("Image", frame)

    # ESC 키를 눌렀을 때 창을 모두 종료하는 부분
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()