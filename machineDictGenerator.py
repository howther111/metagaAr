#jsonデータを読み込んで、駒データを作るプログラム

import json
import csv
import script.machine

def create_machine_dict():
    machine_dict = {}
    with open("./porn_conf.csv", "r", encoding="UTF-8") as csvfile:
        f = csv.reader(csvfile, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"',
                       skipinitialspace=True)

        header = next(f)
        print(header)
        for row in f:
            # rowはList
            # row[0]で必要な項目を取得することができる
            print(row)
