import cv2
import time
import modules.HolisticModule as hm
from win10toast import ToastNotifier


# fps = 1초당 프레임의 수
# privious time for fps
pTime = 0
# cerrent time for fps
cTime = 0

# video input
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

while True:
    # default BGR img
    success, img = cap.read()

    # 웹캠 이미지 반전
    img = detector.findHolistic(cv2.flip(img, 1), draw=True)

    # output -> list ( id, x, y, z) 32 개 좌표인데 예를 들면, (11, x, y, z)
    pose_lmList = detector.findPoseLandmark(img, draw=True)
    # 468개의 얼굴 점 리스트
    face_lmList = detector.findFaceLandmark(img, draw=True)

    # fps 계산 로직
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    my_computer_fps = fps + 1

    # 인체가 감지가 되었는지 확인하는 구문
    if len(pose_lmList) != 0 and len(face_lmList) != 0:

        # Holistic_module에 있는 findDistance의 p2값을 수정하여 사용
        # 왼쪽 center_left_hand 좌표와 얼굴 152번(턱) 좌표를 사용하여 길이를 구하는 부분

        left_hand_len = detector.findPointDistance(152,20)
        right_hand_len = detector.findPointDistance(152, 17)

        # 양 어깨의 관절점 사이의 거리를 이미지로 변경
        shoulder_img = detector.drawShoulder(11,12,img,draw=True)

        # 어깨의 y값 비교하여 양 쪽 어깨의 높이가 다르면 어깨 비대칭으로 인식
        shoulder_hd = detector.findShoulder(11, 12)

        left_hand_img = detector.drawPointDistance(152, 20, img, draw=True)
        right_hand_img = detector.drawPointDistance(152, 17, img, draw=True)

        if left_hand_len < 105 or right_hand_len < 105:
            jaw_bone_count += 1
        else:
            jaw_bone_count = 0

        if shoulder_hd >= 20:
            shoulder_count += 1
        else:
            shoulder_count = 0

        # 3초동안 턱 괴기 자세가 인식되면 알림을 제공한다.
        if jaw_bone_count > my_computer_fps * 3:
            print("WARNING - Please hands down")
            # win10toast 알림 제공
            toaster.show_toast("jaw_bone WARNING", f"Please hands down.\n\n")

            # 알림 제공 후 카운트를 다시 0으로 만든다.
            jaw_bone_count = 0

            real_jaw_bone_count += 1

        if shoulder_count > my_computer_fps * 3:
            print("WARNING - Keep your posture straight.")
            toaster.show_toast("Asymmetric shoulders WARNING",
                               f"Keep your posture straight.")
            # 알림 제공 후 카운트를 다시 0으로 만듬
            shoulder_count = 0

            real_shoulder_count += 1
        print("왼쪽 손 : {:.3f},   오른쪽 손 : {:.3f},    어깨 높이 차 : {:.1f}".format(left_hand_len, right_hand_len, shoulder_hd))

    # fps를 이미지 상단에 입력하는 로직
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    # img를 우리에게 보여주는 부분
    cv2.imshow("Image", img)

    # ESC 키를 눌렀을 때 창을 모두 종료하는 부분
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
