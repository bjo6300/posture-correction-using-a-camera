
import cv2
import mediapipe as mp
import time
import math


class HolisticDetector():
    def __init__(self,
                 static_image_mode=False,
                 model_complexity=1,
                 smooth_landmarks=True,
                 min_detection_confidence=0.5,
                 min_tracking_confidence=0.5):
        self.static_image_mode = static_image_mode
        self.model_complexity = model_complexity
        self.smooth_landmarks = smooth_landmarks
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.mpHolistic = mp.solutions.holistic
        self.mpPose = mp.solutions.pose
        self.mpFace = mp.solutions.face_mesh
        self.holistics = self.mpHolistic.Holistic(self.static_image_mode, self.model_complexity, self.smooth_landmarks,
                                                  self.min_detection_confidence, self.min_tracking_confidence)
        self.mpDraw = mp.solutions.drawing_utils

        self.tipIds = [4, 8, 12, 16, 20]

    def findHolistic(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.holistics.process(imgRGB)

        if self.results.pose_landmarks:

            if draw:
                # Draw pose, left and right hands, and face landmarks on the image.
                annotated_image = img.copy()

                # self.mpDraw.draw_landmarks(
                #     annotated_image, self.results.face_landmarks, self.mpHolistic.FACE_CONNECTIONS)
                # self.mpDraw.draw_landmarks(
                #     annotated_image, self.results.left_hand_landmarks, self.mpHolistic.HAND_CONNECTIONS)
                # self.mpDraw.draw_landmarks(
                #     annotated_image, self.results.right_hand_landmarks, self.mpHolistic.HAND_CONNECTIONS)
                # self.mpDraw.draw_landmarks(
                #     annotated_image, self.results.pose_landmarks, self.mpHolistic.POSE_CONNECTIONS)

                # Plot pose world landmarks.
                # self.mpDraw.plot_landmarks(
                #     self.results.pose_world_landmarks, self.mpHolistic.POSE_CONNECTIONS)
                return annotated_image

        return img

    def findPoseLandmark(self, img, draw=True):
        xList = []
        yList = []

        self.pose_lmList = []
        if self.results.pose_landmarks:
            myHolistic = self.results.pose_landmarks
            # print(myHolistic.landmark)
            # print(type(myHolistic.landmark))
            for id, lm in enumerate(myHolistic.landmark):
                # print(id,lm)
                h, w, c = img.shape
                cx, cy, cz = int(lm.x * w), int(lm.y * h), int(lm.z * (w + h) / 2)
                # print(id, cx, cy)
                # print(cz)
                xList.append(cx)
                yList.append(cy)
                self.pose_lmList.append([id, cx, cy, cz])

        return self.pose_lmList

    def findFaceLandmark(self, img, draw=True):
        xList = []
        yList = []

        self.face_lmList = []
        if self.results.face_landmarks:
            myHolistic = self.results.face_landmarks
            # print(type(myHolistic.landmark))
            for id, lm in enumerate(myHolistic.landmark):
                # print(id,lm)
                h, w, c = img.shape
                cx, cy, cz = int(lm.x * w), int(lm.y * h), int(lm.z * (w + h) / 2)
                # print(id, cx, cy)
                xList.append(cx)
                yList.append(cy)
                self.face_lmList.append([id, cx, cy, cz])

        return self.face_lmList

    def findLefthandLandmark(self, img, draw=True):
        xList = []
        yList = []

        self.left_hand_lmList = []
        if self.results.left_hand_landmarks:
            myHolistic = self.results.left_hand_landmarks
            # print(myHolistic.landmark)
            # print(type(myHolistic.landmark))
            for id, lm in enumerate(myHolistic.landmark):
                # print(id,lm)
                h, w, c = img.shape
                cx, cy, cz = int(lm.x * w), int(lm.y * h), int(lm.z * (w + h) / 2)
                # print(id, cx, cy)
                # print(cz)
                xList.append(cx)
                yList.append(cy)
                self.left_hand_lmList.append([id, cx, cy, cz])

        return self.left_hand_lmList

    def findRighthandLandmark(self, img, draw=True):
        xList = []
        yList = []

        self.right_hand_lmList = []
        if self.results.right_hand_landmarks:
            myHolistic = self.results.right_hand_landmarks
            # print(myHolistic.landmark)
            # print(type(myHolistic.landmark))
            for id, lm in enumerate(myHolistic.landmark):
                # print(id,lm)
                h, w, c = img.shape
                cx, cy, cz = int(lm.x * w), int(lm.y * h), int(lm.z * (w + h) / 2)
                # print(id, cx, cy)
                # print(cz)
                xList.append(cx)
                yList.append(cy)
                self.right_hand_lmList.append([id, cx, cy, cz])

        return self.right_hand_lmList

    def left_hand_fingersUp(self, axis=False):
        fingers = []

        if axis == False:
            # Thumb
            if self.left_hand_lmList[self.tipIds[0]][1] < self.left_hand_lmList[self.tipIds[4]][1]:
                if self.left_hand_lmList[self.tipIds[0]][1] < self.left_hand_lmList[self.tipIds[0] - 2][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            elif self.left_hand_lmList[self.tipIds[0]][1] > self.left_hand_lmList[self.tipIds[4]][1]:
                if self.left_hand_lmList[self.tipIds[0]][1] > self.left_hand_lmList[self.tipIds[0] - 2][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # Fingers except Thumb
            for id in range(1, 5):
                if self.left_hand_lmList[self.tipIds[id]][2] < self.left_hand_lmList[self.tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

        # axis = True( to detect LIKE gesture )
        else:
            # Thumb
            if self.left_hand_lmList[self.tipIds[0]][2] < self.left_hand_lmList[self.tipIds[0] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

            # Fingers except Thumb
            if self.left_hand_lmList[self.tipIds[0]][1] < self.left_hand_lmList[self.tipIds[4]][1]:
                for id in range(1, 5):
                    if self.left_hand_lmList[self.tipIds[id]][1] > self.left_hand_lmList[self.tipIds[id] - 2][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
            else:
                for id in range(1, 5):
                    if self.left_hand_lmList[self.tipIds[id]][1] < self.left_hand_lmList[self.tipIds[id] - 2][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

        return fingers

    def right_hand_fingersUp(self, axis=False):
        fingers = []

        if axis == False:
            # Thumb
            if self.right_hand_lmList[self.tipIds[0]][1] > self.right_hand_lmList[self.tipIds[4]][1]:
                if self.right_hand_lmList[self.tipIds[0]][1] > self.right_hand_lmList[self.tipIds[0] - 2][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            if self.right_hand_lmList[self.tipIds[0]][1] < self.right_hand_lmList[self.tipIds[4]][1]:
                if self.right_hand_lmList[self.tipIds[0]][1] < self.right_hand_lmList[self.tipIds[0] - 2][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # Fingers except Thumb
            for id in range(1, 5):
                if self.right_hand_lmList[self.tipIds[id]][2] < self.right_hand_lmList[self.tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

        # axis = True( to detect LIKE gesture )
        else:
            # Thumb
            if self.right_hand_lmList[self.tipIds[0]][2] < self.right_hand_lmList[self.tipIds[0] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

            # Fingers except Thumb
            if self.right_hand_lmList[self.tipIds[0]][1] < self.right_hand_lmList[self.tipIds[4]][1]:
                for id in range(1, 5):
                    if self.right_hand_lmList[self.tipIds[id]][1] > self.right_hand_lmList[self.tipIds[id] - 2][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
            else:
                for id in range(1, 5):
                    if self.right_hand_lmList[self.tipIds[id]][1] < self.right_hand_lmList[self.tipIds[id] - 2][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

        return fingers

    def findCenter(self, p1, p2):
        x1, y1 = self.pose_lmList[p1][1:3]
        x2, y2 = self.pose_lmList[p2][1:3]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        return cx, cy

    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        x1, y1 = self.face_lmList[p1][1:3]
        # x2, y2 = self.pose_lmList[p2][1:3]
        x2, y2 = p2[0], p2[1]

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)

        return length, img

    def drawEars(self, img, draw=True, r=5, t=1):
        p = [7, 8, 3, 6, 2, 5, 1, 4]
        xy = []
        for i in range(len(p)):
            xy.append(self.pose_lmList[p[i]][1:3])

        if draw:
            # cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            for i in range(len(p)):
                cv2.circle(img, (xy[i][0], xy[i][1]), r, (255, 0, 255), cv2.FILLED)

            for i in range(int(len(p)/2-1)):
                num = 2 * i
                cv2.line(img, (xy[num][0], xy[num][1]), (xy[num+2][0], xy[num+2][1]), (255, 0, 255), t)
                cv2.line(img, (xy[num+1][0], xy[num+1][1]), (xy[num+3][0], xy[num+3][1]), (255, 0, 255), t)

        return img

    def drawShoulder2(self, img, draw=True, r=5, t=2):
        p = [11, 12, 13, 14, 19, 20]
        xy = []
        for i in range(len(p)):
            xy.append(self.pose_lmList[p[i]][1:3])

        if draw:
            for i in range(len(p)):
                cv2.circle(img, (xy[i][0], xy[i][1]), r, (255, 0, 255), cv2.FILLED)

            cv2.line(img, (xy[0][0], xy[0][1]), (xy[1][0], xy[1][1]), (255, 0, 255), t)
            cv2.line(img, (xy[0][0], xy[0][1]), (xy[2][0], xy[2][1]), (255, 0, 255), t)
            cv2.line(img, (xy[2][0], xy[2][1]), (xy[4][0], xy[4][1]), (255, 0, 255), t)
            cv2.line(img, (xy[1][0], xy[1][1]), (xy[3][0], xy[3][1]), (255, 0, 255), t)
            cv2.line(img, (xy[3][0], xy[3][1]), (xy[5][0], xy[5][1]), (255, 0, 255), t)
            # cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            # cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            # cv2.circle(img, (x3, y3), r, (255, 0, 255), cv2.FILLED)
            # cv2.circle(img, (x4, y4), r, (255, 0, 255), cv2.FILLED)
            # cv2.circle(img, (x5, y5), r, (255, 0, 255), cv2.FILLED)
            # cv2.circle(img, (x6, y6), r, (255, 0, 255), cv2.FILLED)

        return img

    def drawMouth(self, img, draw=True, r=3, t=1):

        p = [135, 169, 170, 140, 171, 175, 396, 400, 378, 379, 365, 397]
        xy = []
        for i in range(len(p)):
            xy.append(self.face_lmList[p[i]][1:3])

        if draw:
            for i in range(len(p)):
                # cv2.circle(img, (xy[i][0], xy[i][1]), r, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (xy[i][0], xy[i][1]), r, (0, 255, 0), cv2.FILLED)
        if draw:
            for i in range(len(p)-1):
                # cv2.line(img, (xy[i][0], xy[i][1]), (xy[i + 1][0], xy[i + 1][1]), (255, 255, 255), 1)
                cv2.line(img, (xy[i][0], xy[i][1]), (xy[i + 1][0], xy[i + 1][1]), (0, 255, 0), 1)
        return img

    def findPointDistance2(self, p1, p2):
        x1, y1 = self.pose_lmList[p1][1:3]
        x2, y2 = self.pose_lmList[p2][1:3]

        length = math.hypot(x2 - x1, y2 - y1)

        return length

    # 관절점 사이 기울기 구하기
    def findinclination(self, p1, p2):
        x1, y1 = self.pose_lmList[p1][1:3]
        x2, y2 = self.pose_lmList[p2][1:3]

        if (x2 - x1) == 0:
            print("기울기 오류")
            return 0

        inclination = (y2 - y1) / (x2 - x1)
        return inclination

    # 추가된 함수
    # 얼굴 관절점과 포즈 관절점을 시각화하여 보여주고
    # 둘의 거리차만큼 선으로 연결하여 그것을 시각화하여 보여줌
    def drawPointDistance(self, p1, p2, img, draw=True, r=5, t=1):
        x1, y1 = self.face_lmList[p1][1:3]
        x2, y2 = self.pose_lmList[p2][1:3]
        # x2, y2 = p2[0],p2[1]

        if draw:
            # cv2.line(img, (x1, y1), (x2, y2), (171, 242, 0), t)
            # cv2.circle(img, (x1, y1), r, (171, 242, 0), cv2.FILLED)
            # cv2.circle(img, (x2, y2), r, (171, 242, 0), cv2.FILLED)
            cv2.circle(img, (x1, y1), r, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (0, 255, 0), cv2.FILLED)

        return img

    # 추가된 함수
    # 얼굴 관절점과 포즈 관절점의 거리 차 구하기
    def findPointDistance(self, p1, p2):
        x1, y1 = self.face_lmList[p1][1:3]
        x2, y2 = self.pose_lmList[p2][1:3]

        length = math.hypot(x2 - x1, y2 - y1)

        # cv2.putText(img, str(int(length)), (x2 - 50, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

        return length

    # 추가된 함수
    # 얼굴 관절점과 포즈 관절점의 거리 차 구하기
    def findMouthDistance(self, img, p1, p2):
        x1, y1 = self.face_lmList[p1][1:3]
        x2, y2 = self.face_lmList[p2][1:3]

        length = math.hypot(x2 - x1, y2 - y1)

        # cv2.putText(img, str(int(length)), (x2 - 50, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        # cv2.putText(img, str(int(length)), (x2 - 50, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        return length

    # 추가된 함수
    # 어깨의 두 점 11, 12의 점과 사이 라인 표시
    def drawShoulder(self, p1, p2, img, draw=True, r=5, t=2):
        x1, y1 = self.pose_lmList[p1][1:3]
        x2, y2 = self.pose_lmList[p2][1:3]

        if draw:
            # cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            # cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            # cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), t)
            cv2.circle(img, (x1, y1), r, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (0, 255, 0), cv2.FILLED)

        return img

    # 추가된 함수
    # 11, 12번 점의 y 값의 차 구하기
    def findShoulder(self, p1, p2):
        x1, y1 = self.pose_lmList[p1][1:3]
        x2, y2 = self.pose_lmList[p2][1:3]

        if y1 > y2:
            return y1 - y2
        elif y1 < y2:
            return y2 - y1
        elif y1 == y2:
            return 0
        else:
            print("어깨 오류 발생")

    def findDepth(self, p1, p2):
        depth = abs((self.pose_lmList[p1][3] + self.pose_lmList[p2][3]) / 2)
        return depth

    def findEyeBlink(self, p1, p2, img, draw=True, r=15, t=3):
        x1, y1 = self.face_lmList[p1][1:3]
        x2, y2 = self.face_lmList[p2][1:3]

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)

        return length, img

    def findEyeDepth(self, p1, p2):
        depth = abs((self.face_lmList[p1][3] + self.face_lmList[p2][3]) / 2)
        return depth

    def drawLine(self, p1, p2, img, t=3):
        x1, y1 = self.face_lmList[p1][1:3]
        x2, y2 = self.face_lmList[p2][1:3]

        cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), t)

    def findLength_lh_rh(self, p1, p2):
        x1, y1 = self.left_hand_lmList[p2][1:3]
        x2, y2 = self.right_hand_lmList[p1][1:3]

        length = math.hypot(abs(x2 - x1), abs(y2 - y1))
        return length

    def findLength_lh_lh(self, p1, p2):
        x1, y1 = self.left_hand_lmList[p2][1:3]
        x2, y2 = self.left_hand_lmList[p1][1:3]

        length = math.hypot(abs(x2 - x1), abs(y2 - y1))
        return length

    def findLength_rh_rh(self, p1, p2):
        x1, y1 = self.right_hand_lmList[p2][1:3]
        x2, y2 = self.right_hand_lmList[p1][1:3]

        length = math.hypot(abs(x2 - x1), abs(y2 - y1))
        return length

    def findLength_pose(self, p1, p2):
        x1, y1 = self.pose_lmList[p2][1:3]
        x2, y2 = self.pose_lmList[p1][1:3]

        length = math.hypot(abs(x2 - x1), abs(y2 - y1))
        return length

    def findAngle(self, img, p1, p2, p3, draw=True):
        # 랜드마크 좌표 얻기
        # , x1, y1 = self.lmList[p1]
        x1, y1 = self.face_lmList[p1][1:3]
        x2, y2 = self.face_lmList[p2][1:3]
        x3, y3 = self.face_lmList[p3][1:3]

        # 각도 계산
        radian = math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2)
        angle = math.degrees(radian)

        if angle < 0:
            angle += 360

        # print(angle)
        # 점, 선 그리기
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x2, y2), (x3, y3), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 5, (0, 0, 255), cv2.FILLED)
            # cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 5, (0, 0, 255), cv2.FILLED)
            # cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 5, (0, 0, 255), cv2.FILLED)
            # cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            # cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            cv2.putText(img, str(int(angle)), (20, 40), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 255), 2)
            cv2.putText(img, "jaw angle", (20, 60), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 255), 1)

        return angle

    def findMouthAngle(self, img, p1, p2, p3, draw=True):
        # 랜드마크 좌표 얻기
        # , x1, y1 = self.lmList[p1]
        x1, y1 = self.face_lmList[p1][1:3]
        x2, y2 = self.face_lmList[p2][1:3]
        x3, y3 = self.face_lmList[p3][1:3]

        # 각도 계산
        radian = math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2)
        angle = math.degrees(radian)

        if angle < 0:
            angle += 360

        # print(angle)
        # 점, 선 그리기
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x2, y2), (x3, y3), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 5, (0, 0, 255), cv2.FILLED)
            # cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 5, (0, 0, 255), cv2.FILLED)
            # cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 5, (0, 0, 255), cv2.FILLED)
            # cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            # cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            cv2.putText(img, str(int(angle)), (20, 40), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 255), 2)
            cv2.putText(img, "mouse angle", (20, 60), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 255), 1)

        return angle

    def findHandAngle(self, img, p1, p2, p3, draw=True):
        # 랜드마크 좌표 얻기
        # , x1, y1 = self.lmList[p1]
        x1, y1 = self.right_hand_lmList[p1][1:3]
        x2, y2 = self.right_hand_lmList[p2][1:3]
        x3, y3 = self.right_hand_lmList[p3][1:3]

        # 각도 계산
        radian = math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2)
        angle = math.degrees(radian)

        if angle < 0:
            angle += 360

        # print(angle)
        # 점, 선 그리기
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x2, y2), (x3, y3), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            # cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

        return angle

