### マーカーIDと、動画を重ねて表示する
import cv2
from cv2 import aruco
import time


class markerPoint:
    corners = []
    id = []

### --- aruco設定 --- ###
dict_aruco = aruco.Dictionary_get(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters_create()
window_baisu = 1
hanten_flg = False

cap = cv2.VideoCapture(0)

try:
    while True:
        ret, frame = cap.read()

        if hanten_flg:
            frame = cv2.rotate(frame, cv2.ROTATE_180)

        # image画像から大きさ情報を取得する。(image_colorは使用しないです。)
        image_hight, image_width, image_color = frame.shape

        # windowを名前付きで作成: nameは任意のstring; WINDOW_NORMALなら次のサイズ調整が可能 AUTO
        cv2.namedWindow('frame', cv2.WINDOW_NORMAL)

        # image画像を2倍にする。
        cv2.resizeWindow('frame', image_width * window_baisu, image_hight * window_baisu)

        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, dict_aruco, parameters=parameters)
        points = []
        idcount = 0

        points = []
        for i in range(len(ids)):
            point = markerPoint()
            point.corners = corners[i]
            point.id = ids[i]
            points.append(point)

        for point in points:
            print(point.corners[0])
            #print(cor)
            center_x = (point.corners[0][0][0] + point.corners[0][1][0]
                        + point.corners[0][2][0] + point.corners[0][3][0]) / 4
            center_y = (point.corners[0][0][1] + point.corners[0][1][1]
                        + point.corners[0][2][1] + point.corners[0][3][1]) / 4
            print("id = " + str(point.id[0]))
            print("center_x = " + str(center_x))
            print("center_y = " + str(center_y))

        #print(corners)
        print(ids)



        frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
        cv2.imshow('frame', frame_markers)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyWindow('frame')
    cap.release()
except KeyboardInterrupt:
    cv2.destroyWindow('frame')
    cap.release()