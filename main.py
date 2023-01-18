# This is a sample Python script.
import cv2.aruco

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from arreadtest9 import imgToBoard

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    test = imgToBoard(spread_sheet_url='https://docs.google.com/spreadsheets/d/1VQw8wQCI6WHVaMuSCLhoxGHVNA5ZUNzxbhP-_vfpWpM')
    test.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
