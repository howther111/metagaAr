# This is a sample Python script.
import cv2
from cv2 import aruco
from arreadtest10 import imgToBoard
import csv

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    test = imgToBoard(dict_aruco=aruco.DICT_4X4_50)
    #test.run()
    try:
        while True:
            ret_porn_list = test.output_to_csv()

            if ret_porn_list != None:
                with open('porn_list.csv', 'w') as csvfile:
                    writer = csv.writer(csvfile, lineterminator='\n')

                    for porn in ret_porn_list:
                        writer.writerow([porn.id, porn.x_zahyo, porn.y_zahyo])

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except:
        pass


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
