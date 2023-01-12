import cv2


hanten_flg = False
window_baisu = 2

cap = cv2.VideoCapture(0)

#繰り返しのためのwhile文
while True:
    #カメラからの画像取得
    ret, frame = cap.read()
    # image画像から大きさ情報を取得する。(image_colorは使用しないです。)
    image_hight, image_width, image_color = frame.shape

    # windowを名前付きで作成: nameは任意のstring; WINDOW_NORMALなら次のサイズ調整が可能 AUTO
    cv2.namedWindow('camera', cv2.WINDOW_NORMAL)

    # image画像を2倍にする。
    cv2.resizeWindow('camera', image_width * window_baisu, image_width * window_baisu)


    if hanten_flg:
        frame = cv2.rotate(frame, cv2.ROTATE_180)

    #カメラの画像の出力
    cv2.imshow('camera' , frame)

    #繰り返し分から抜けるためのif文
    key =cv2.waitKey(10)
    if key == 27:
        break

#メモリを解放して終了するためのコマンド
cap.release()
cv2.destroyAllWindows()