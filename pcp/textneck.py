import cv2
import time

import numpy as np

import modules.HolisticModule as hm
from win10toast import ToastNotifier
import tensorflow as tf
import keras.models
from keras.utils import np_utils
from keras.models import Sequential
from keras.preprocessing.image import img_to_array
from PIL import Image

# fps = 1초당 프레임의 수
# privious time for fps
pTime = 0
# cerrent time for fps
cTime = 0

model = tf.keras.models.load_model('saved_model')

# video input
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Holistic 객체(어떠한 행위를 하는 친구) 생성
detector = hm.HolisticDetector()

# toast 알림을 주는 객체 생성
toaster = ToastNotifier()

# 거북목 변수 초기 세팅
text_neck_count = 0

# 실제 거북목 변수 초기 세팅
real_text_neck_count = 0


while True:

    # default BGR img
    success, frame = cap.read()

    # 웹캠 이미지 반전
    img = detector.findHolistic(cv2.flip(frame, 1), draw=True)

    # output -> list ( id, x, y, z) 32 개 좌표인데 예를 들면, (11, x, y, z)
    pose_lmList = detector.findPoseLandmark(frame, draw=True)
    # 468개의 얼굴 점 리스트
    face_lmList = detector.findFaceLandmark(frame, draw=True)

    # fps 계산 로직
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    my_computer_fps = fps + 1

    turtleNeck_frame = cv2.imwrite('frame.jpg', frame)

    file_link = "frame.jpg"

    # 인체가 감지가 되었는지 확인하는 구문
    if len(pose_lmList) != 0 and len(face_lmList) != 0:

        img = Image.open(file_link)
        img = img.convert("RGB")
        img = img.resize((64,64))

        turtleNeck_region = img_to_array(img)
        turtleNeck_region = np.expand_dims(turtleNeck_region,axis=0)

        single_test = model.predict(turtleNeck_region)

        if single_test == 1:
            text_neck_count += 1
        else:
            text_neck_count = 0

        if text_neck_count > my_computer_fps * 3:
            print("WARNING - turtle neck warning")
            # win10toast 알림 제공
            toaster.show_toast("turtle neck WARNING", f"Please hands down.\n\n")

            # 알림 제공 후 카운트를 다시 0으로 만든다.
            text_neck_count = 0

            real_text_neck_count += 1

        print("거북목 정확도 :",single_test[0][0])

    # fps를 이미지 상단에 입력하는 로직
    cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    # img를 우리에게 보여주는 부분
    cv2.imshow("Image", frame)

    # ESC 키를 눌렀을 때 창을 모두 종료하는 부분
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()