### マーカーIDと、動画を重ねて表示する
import cv2
from cv2 import aruco
import time

### --- aruco設定 --- ###
dict_aruco = aruco.Dictionary_get(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters_create()
window_baisu = 2
hanten_flg = True

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
        cv2.resizeWindow('frame', image_width * window_baisu, image_width * window_baisu)

        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, dict_aruco, parameters=parameters)

        print(corners)
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