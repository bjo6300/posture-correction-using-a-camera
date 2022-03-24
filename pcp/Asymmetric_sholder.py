import cv2
import time
import HolisticModule as hm
from win10toast import ToastNotifier

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

# sholder count, hd(height difference) 변수 생성
sholder_count = 0
sholder_hd = 0


def printSholder(t):
    print("Sholder Height Difference : {}".format(t))


while True:
    # defalut BGR img
    success, img = cap.read()

    # mediapipe를 거친 이미지 생성 -> img
    img = detector.findHolistic(img, draw=True)

    # 웹캠 이미지 반전
    img = cv2.flip(img, 1)

    # output -> list (id, x, y, z) 32 개 좌표인데 예를 들면, (11, x, y, z)
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

        # 어깨의 점과 길이가 표시된 이미지로 변경
        img = detector.drawSholder(11, 12, img, draw=True)

        # 어깨의 y값 비교하여 양 쪽 어깨의 높이가 다르면 어깨 비대칭으로 인식
        sholder_hd = detector.findSholder(11, 12)

        if sholder_hd >= 20:
            sholder_count += 1
        else:
            sholder_count = 0

        # 100번 어깨 비대칭으로 인식되면 알림을 제공
        if sholder_count > my_computer_fps * 3:
            print("WARNING - Keep your posture straight.")
            toaster.show_toast("Asymmetric shoulders WARNING",
                               f"Keep your posture straight.")
            # 알림 제공 후 카운트를 다시 0으로 만듬
            sholder_count = 0
        printSholder(sholder_hd)

    # fps를 이미지 상단에 입력하는 로직
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    # putText(이미지파일, 출력 문자, 출력 문자 좌표, 폰트, 크기, 색, 두께)
    # img를 우리에게 보여주는 부분
    cv2.imshow("Image", img)

    # ESC 키를 눌렀을 때 창을 모두 종료하는 부분
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

