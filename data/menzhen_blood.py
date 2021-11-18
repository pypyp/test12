# coding=UTF-8
import os
import sys

sys.path.append(r'' + os.path.abspath('../'))
import json
from common.yaml_util import read_mz_blood_yaml,read_csv,read_yaml
import time

class mz_blood:

    '''
    添加血糖测试用例
    '''

    def add_zy_glu0(self):  # 添加血糖
        data = json.dumps({
            "userId": read_mz_blood_yaml()['userId'],
            "value": 5,
            "valueUnit": 1,
            "method": 0,
            "nurseId": read_yaml('userId'),
            "timeType": "空腹",
            "measureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "unusual": 1,
            "comment": "门诊zdh0"
        })
        return data

    def add_zy_glu1(self):  # 添加血糖

        data = json.dumps({
            "userId": read_mz_blood_yaml()['userId'],
            "value": 33.3,
            "valueUnit": 1,
            "method": 0,
            "nurseId": read_yaml('userId'),
            "timeType": "早餐后",
            "measureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "unusual": 2,
            "comment": "门诊zdh0"

            })
        return data

    def add_zy_glu2(self):  # 添加血糖

        data = json.dumps({
            "userId": read_mz_blood_yaml()['userId'],
            "value": 0.6,
            "valueUnit": 1,
            "method": 0,
            "nurseId": read_yaml('userId'),
            "timeType": "午餐前",
            "measureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "unusual": 0,
            "comment": "门诊zdh2"})
        return data

    def add_zy_glu3(self):  # 添加血糖

        data = json.dumps({
            "userId": read_mz_blood_yaml()['userId'],
            "valueUnit": 1,
            "method": 0,
            "nurseId": read_yaml('userId'),
            "timeType": "午餐后",
            "measureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "unusual": 3,
            "comment": "门诊zdh3"
        })
        return data

    def add_zy_glu4(self):  # 添加血糖

        data = json.dumps({
            "userId": read_mz_blood_yaml()['userId'],
            "valueUnit": 1,
            "method": 0,
            "nurseId": read_yaml('userId'),
            "timeType": "晚餐前",
            "measureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "unusual": 4,
            "comment": "门诊zdh4"
        })
        return data

    def add_zy_glu5(self):  # 添加血糖

        data = json.dumps({
            "userId": read_mz_blood_yaml()['userId'],
            "valueUnit": 1,
            "method": 0,
            "nurseId": read_yaml('userId'),
            "timeType": "晚餐后",
            "measureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "unusual": 5,
            "comment": "门诊zdh5"
        })
        return data

    def add_zy_glu6(self):  # 添加血糖

        data = json.dumps({
            "userId": read_mz_blood_yaml()['userId'],
            "valueUnit": 1,
            "method": 0,
            "nurseId": read_yaml('userId'),
            "timeType": "随机",
            "measureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "unusual": 6,
            "comment": "门诊zdh6"
        })
        return data

    def add_zy_glu7(self):  # 添加血糖

        data = json.dumps({
            "userId": read_mz_blood_yaml()['userId'],
            "valueUnit": 1,
            "method": 0,
            "nurseId": read_yaml('userId'),
            "timeType": "随机",
            "measureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "unusual": 7,
            "comment": "门诊zdh7"
        })
        return data

    def add_zy_glu8(self):  # 添加血糖

        data = json.dumps({
            "userId": read_mz_blood_yaml()['userId'],
            "valueUnit": 1,
            "method": 0,
            "nurseId": read_yaml('userId'),
            "timeType": "q3h",
            "measureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "unusual": 8,
            "comment": "门诊zdh8"
        })
        return data

    def add_zy_glu9(self):  # 添加血糖

        data = json.dumps({
            "userId": read_mz_blood_yaml()['userId'],
            "valueUnit": 1,
            "method": 0,
            "nurseId": read_yaml('userId'),
            "timeType": "随机",
            "measureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "unusual": 9,
            "comment": "门诊zdh9"
        })
        return data

    def menzhen_patient_glu(self):  #血糖
        data = json.dumps({
            "userId": (read_mz_blood_yaml()['userId']),
            "pageNo": 1,
            "orderBy": "id desc",
            "pageSize": 20
        })
        return data


    '''
    更新患者血糖测试用例，更新时段，更新血糖值
    '''
    def menzhen_patient_glu_update1(self):  #更新患者血糖时段
        data = json.dumps({
                "comment": "测试",
                "id": read_mz_blood_yaml()['id'],
                "measureTime": read_mz_blood_yaml()['measureTime'],
                "method": 0,
                "value": 6.2,
                "nurseId": read_yaml('userId'),
                "timeType": "随机",
                "unusual": 1,
                "userId": read_mz_blood_yaml()["userId"],
                "valueUnit": 1,
            })
        return data

    def menzhen_patient_glu_update2(self):  #更新患者血糖值
        data = json.dumps({
                "comment": "测试",
                "id": read_mz_blood_yaml()['id'],
                "measureTime": read_mz_blood_yaml()['measureTime'],
                "method": 0,
                "value": 8,
                "nurseId": read_yaml('userId'),
                "timeType": "随机",
                "unusual": 2,
                "userId": read_mz_blood_yaml()["userId"],
                "valueUnit": 1,
            })
        return data

    '''
    删除血糖测试用例
    '''
    def menzhen_patient_glu_del(self):  #删除血糖
        data = json.dumps({
                "id": read_mz_blood_yaml()['id'],

            })
        return data