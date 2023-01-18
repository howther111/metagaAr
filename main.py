# This is a sample Python script.
import cv2
from cv2 import aruco
from arreadtest11 import imgToBoard
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
    ret_porn_dict = {}
    try:
        while True:
            ret_porn_dict = test.output_to_csv(ret_porn_dict=ret_porn_dict)

            if ret_porn_dict != {}:
                with open('porn_list.csv', 'w') as csvfile:
                    writer = csv.writer(csvfile, lineterminator='\n')

                    for key in ret_porn_dict.keys():
                        print(key)
                        print(ret_porn_dict[key].x_zahyo)
                        print(ret_porn_dict[key].y_zahyo)
                        writer.writerow([key, ret_porn_dict[key].x_zahyo, ret_porn_dict[key].y_zahyo])

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except:
        pass
        #raise Exception


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
