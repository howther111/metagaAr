### マーカーIDと、動画を重ねて表示する
import math

import cv2
from cv2 import aruco
import time
import setting
import gspread

class markerPoint:
    corners = []
    id = []

class markerInfo:
    id = 999
    zahyo = ""

### --- aruco設定 --- ###
dict_aruco = aruco.Dictionary_get(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters_create()
window_baisu = 1
hanten_flg = False

cap = cv2.VideoCapture(0)
#ワークブックの認証
wb = gspread.service_account(filename="./service_account.json")
#URLで指定
sheet = wb.open_by_url('https://docs.google.com/spreadsheets/d/1VQw8wQCI6WHVaMuSCLhoxGHVNA5ZUNzxbhP-_vfpWpM')
sheet2 = sheet.worksheet("AR連携表")
#print(sheet2.get('A2'))
#title = wb.title
#print(title)

# 認証処理
#gc = gspread.authorize(creds)

try:
    #四隅のコーナーの位置を記録
    x_cell_num = setting.x_cell_num
    y_cell_num = setting.y_cell_num
    left_up_corner_x = 0.0
    left_up_corner_y = 0.0
    left_up_corner_id = 0
    right_up_corner_x = 100.0
    right_up_corner_y = 0.0
    right_up_corner_id = 1
    left_down_corner_x = 0.0
    left_down_corner_y = 100.0
    left_down_corner_id = 2
    right_down_corner_x = 100.0
    right_down_corner_y = 100.0
    right_down_corner_id = 3

    map_width = 100.0
    map_height = 100.0

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
            #print(point.corners[0])
            center_x = (point.corners[0][0][0] + point.corners[0][1][0]
                        + point.corners[0][2][0] + point.corners[0][3][0]) / 4
            center_y = (point.corners[0][0][1] + point.corners[0][1][1]
                        + point.corners[0][2][1] + point.corners[0][3][1]) / 4
            print("id = " + str(point.id[0]))
            print("center_x = " + str(center_x))
            print("center_y = " + str(center_y))
            if point.id[0] == left_up_corner_id:
                left_up_corner_x = center_x
                left_up_corner_y = center_y
            elif point.id[0] == right_up_corner_id:
                right_up_corner_x = center_x
                right_up_corner_y = center_y
            elif point.id[0] == left_down_corner_id:
                left_down_corner_x = center_x
                left_down_corner_y = center_y
            elif point.id[0] == right_down_corner_id:
                right_down_corner_x = center_x
                right_down_corner_y = center_y
            else:
                x_left = (left_up_corner_x + left_down_corner_x) / 2
                x_cell = map_width / setting.x_cell_num
                x_zahyo = math.ceil((center_x - x_left) / x_cell)

                num2alpha = lambda c: chr(c + 64)
                y_up = (left_up_corner_y + right_up_corner_y) / 2
                y_cell = map_height / setting.y_cell_num
                y_zahyo = math.ceil((center_y - y_up) / y_cell)
                print("zahyo = " + str(x_zahyo) + "-" + num2alpha(y_zahyo))
                sscell_x = "B" + (str(point.id[0] - 2))
                sscell_y = "C" + (str(point.id[0] - 2))
                sheet2.update(sscell_x, x_zahyo)
                sheet2.update(sscell_y, y_zahyo)
                time.sleep(2)

        map_width = ((right_up_corner_x - left_up_corner_x)
                     + (right_down_corner_x - left_down_corner_x)) / 2
        map_height = ((right_down_corner_y - right_up_corner_y)
                     + (left_down_corner_y - left_up_corner_y)) / 2
        print("map_width = " + str(map_width))
        print("map_height = " + str(map_height))

        #無ければ追加、あれば移動（削除はしない）
        #print(corners)
        #print(ids)

        frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
        cv2.imshow('frame', frame_markers)
        time.sleep(1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyWindow('frame')
    cap.release()
except KeyboardInterrupt:
    cv2.destroyWindow('frame')
    cap.release()