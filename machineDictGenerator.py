#jsonデータを読み込んで、駒データを作るプログラム

import csv
from script import machineData
import time

def create_machine_dict(porn_conf="./porn_conf.csv"):
    machine_dict = {}
    with open(porn_conf, "r", encoding="UTF-8") as csvfile:
        f = csv.reader(csvfile, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"',
                       skipinitialspace=True)

        header = next(f)
        print(header)
        for row in f:
            # rowはList
            # row[0]で必要な項目を取得することができる
            print(row)
            machine = machineData.Machine(porn_id=row[0], name=row[1],
                                          soeji=row[2], e_or_p=row[3],
                                          jyoutai=row[4], x=0, y=0)
            machine_dict[row[0]] = machine

def update_machine_dict(porn_list="./porn_list.csv", machine_dict={}):
    with open(porn_list, "r", encoding="UTF-8") as csvfile:
        f = csv.reader(csvfile, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"',
                       skipinitialspace=True)
        for row in f:
            # rowはList
            # row[0]で必要な項目を取得することができる
            print(row)
            try:
                machine_dict[row[0]].x = row[1]
                machine_dict[row[0]].y = row[2]
            except:
                pass

        time.sleep(1)

    return machine_dict
