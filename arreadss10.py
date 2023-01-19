### マーカーIDと、動画を重ねて表示する
import math

import cv2
from cv2 import aruco
import time
import settings
import gspread

class markerPoint:
    corners = []
    id = []

class markerInfo:
    id = 999
    x_zahyo = ""
    y_zahyo = ""

class imgToBoard:
    def __init__(self, window_baisu=1,
                 hanten_flg=False, cap=cv2.VideoCapture(0), spread_sheet_url="",
                 account_json="./service_account.json", ar_sheet_name="AR連携表",
                 x_cell_num=9, y_cell_num=6, dict_aruco=aruco.DICT_4X4_50
                 ) -> None:
        self.dict_aruco = aruco.Dictionary_get(dict_aruco)
        self.parameters = aruco.DetectorParameters_create()
        self.window_baisu = window_baisu
        self.hanten_flg = hanten_flg
        # ワークブックの認証
        wb = gspread.service_account(filename=account_json)
        self.sp_sheet = wb.open_by_url(spread_sheet_url)
        self.ar_sheet = self.sp_sheet.worksheet(ar_sheet_name)
        # 四隅のコーナーの位置を記録
        self.x_cell_num = x_cell_num
        self.y_cell_num = y_cell_num
        self.left_up_corner_x = 0.0
        self.left_up_corner_y = 0.0
        self.left_up_corner_id = 0
        self.right_up_corner_x = 100.0
        self.right_up_corner_y = 0.0
        self.right_up_corner_id = 1
        self.left_down_corner_x = 0.0
        self.left_down_corner_y = 100.0
        self.left_down_corner_id = 2
        self.right_down_corner_x = 100.0
        self.right_down_corner_y = 100.0
        self.right_down_corner_id = 3
        self.map_width = 100.0
        self.map_height = 100.0
        self.cap = cap

    def run(self):
        try:
            porn_dict = {}

            while True:
                ret, frame = self.cap.read()

                if self.hanten_flg:
                    frame = cv2.rotate(frame, cv2.ROTATE_180)

                # image画像から大きさ情報を取得する。(image_colorは使用しないです。)
                image_hight, image_width, image_color = frame.shape

                # windowを名前付きで作成: nameは任意のstring; WINDOW_NORMALなら次のサイズ調整が可能 AUTO
                cv2.namedWindow('frame', cv2.WINDOW_NORMAL)

                # image画像を2倍にする。
                cv2.resizeWindow('frame', image_width * self.window_baisu, image_hight * self.window_baisu)

                gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

                corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, self.dict_aruco, parameters=self.parameters)
                points = []
                idcount = 0

                points = []
                for i in range(len(ids)):
                    point = markerPoint()
                    point.corners = corners[i]
                    point.id = ids[i]
                    points.append(point)

                for point in points:
                    # print(point.corners[0])
                    center_x = (point.corners[0][0][0] + point.corners[0][1][0]
                                + point.corners[0][2][0] + point.corners[0][3][0]) / 4
                    center_y = (point.corners[0][0][1] + point.corners[0][1][1]
                                + point.corners[0][2][1] + point.corners[0][3][1]) / 4
                    #print("id = " + str(point.id[0]))
                    #print("center_x = " + str(center_x))
                    #print("center_y = " + str(center_y))
                    if point.id[0] == self.left_up_corner_id:
                        self.left_up_corner_x = center_x
                        self.left_up_corner_y = center_y
                    elif point.id[0] == self.right_up_corner_id:
                        self.right_up_corner_x = center_x
                        self.right_up_corner_y = center_y
                    elif point.id[0] == self.left_down_corner_id:
                        self.left_down_corner_x = center_x
                        self.left_down_corner_y = center_y
                    elif point.id[0] == self.right_down_corner_id:
                        self.right_down_corner_x = center_x
                        self.right_down_corner_y = center_y
                    else:
                        x_left = (self.left_up_corner_x + self.left_down_corner_x) / 2
                        x_cell = self.map_width / self.x_cell_num
                        x_zahyo = math.ceil((center_x - x_left) / x_cell)
                        if x_zahyo < 1 or x_zahyo > self.x_cell_num:
                            x_zahyo = 0

                        num2alpha = lambda c: chr(c + 64)
                        y_up = (self.left_up_corner_y + self.right_up_corner_y) / 2
                        y_cell = self.map_height / self.y_cell_num
                        y_zahyo = math.ceil((center_y - y_up) / y_cell)
                        if y_zahyo < 1 or y_zahyo > self.y_cell_num:
                            y_zahyo = 0

                        if point.id[0] not in porn_dict:
                            newMarkerInfo = markerInfo()
                            newMarkerInfo.id = point.id[0]
                            newMarkerInfo.x_zahyo = x_zahyo
                            newMarkerInfo.y_zahyo = y_zahyo
                            porn_dict[point.id[0]] = newMarkerInfo
                        else:
                            oldMarkerInfo = porn_dict[point.id[0]]
                            if oldMarkerInfo.x_zahyo != x_zahyo or oldMarkerInfo.y_zahyo != y_zahyo:
                                porn_dict[point.id[0]].x_zahyo = x_zahyo
                                porn_dict[point.id[0]].y_zahyo = y_zahyo
                                print("id = " + str(point.id[0]) + ", zahyo = " + str(x_zahyo) + "-" + num2alpha(y_zahyo))
                                sscell_x = "B" + (str(point.id[0] - 2))
                                sscell_y = "C" + (str(point.id[0] - 2))
                                self.ar_sheet.update(sscell_x, x_zahyo)
                                self.ar_sheet.update(sscell_y, y_zahyo)
                                time.sleep(2)

                self.map_width = ((self.right_up_corner_x - self.left_up_corner_x)
                                  + (self.right_down_corner_x - self.left_down_corner_x)) / 2
                self.map_height = ((self.right_down_corner_y - self.right_up_corner_y)
                                   + (self.left_down_corner_y - self.left_up_corner_y)) / 2
                #print("map_width = " + str(self.map_width))
                #print("map_height = " + str(self.map_height))

                # 無ければ追加、あれば移動（削除はしない）
                # print(corners)
                # print(ids)

                frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
                cv2.imshow('frame', frame_markers)
                time.sleep(1)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cv2.destroyWindow('frame')
            self.cap.release()

        except KeyboardInterrupt:
            cv2.destroyWindow('frame')
            self.cap.release()