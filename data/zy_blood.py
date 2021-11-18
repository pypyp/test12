# coding=UTF-8
import os
import sys

sys.path.append(r'' + os.path.abspath('../'))
import json
from common.yaml_util import read_zy_blood_yaml, read_csv, read_zy_yaml, read_bastase_sql, read_yaml
from common.open_database import MysqlDb
import time


class zy_blood:
    '''
    添加血糖测试用例
    '''

    def add_zy_glu0(self):  # 添加血糖
        data = json.dumps({
            "userId": read_zy_yaml()['userId'],
            "value": 5,
            "valueUnit": 1,
            "method": 0,
            "nurseId": read_yaml('userId'),
            "timeType": "空腹",
            "measureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "unusual": 1,
            "comment": "zdh0"
        })
        return data

    def add_zy_glu1(self):  # 添加血糖

        data = json.dumps({
            "userId": read_zy_yaml()['userId'],
            "value": 33.3,
            "valueUnit": 1,
            "method": 0,
            "nurseId": read_yaml('userId'),
            "timeType": "早餐后",
            "measureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "unusual": 2,
            "comment": "zdh1"})
        return data

    def add_zy_glu2(self):  # 添加血糖

        data = json.dumps({
            "userId": read_zy_yaml()['userId'],
            "value": 0.6,
            "valueUnit": 1,
            "method": 0,
            "nurseId": read_yaml('userId'),
            "timeType": "早餐后",
            "measureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "unusual": 0,
            "comment": "zdh2"})
        return data



    def add_zy_glu3(self):  # 添加血糖

        data = json.dumps({
            "userId": read_zy_yaml()['userId'],
            "valueUnit": 1,
            "method": 0,
            "nurseId": read_yaml('userId'),
            "timeType": "午餐前",
            "measureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "unusual": 3,
            "comment": "zdh3"
        })
        return data

    def add_zy_glu4(self):  # 添加血糖

        data = json.dumps({
            "userId": read_zy_yaml()['userId'],
            "valueUnit": 1,
            "method": 0,
            "nurseId": read_yaml('userId'),
            "timeType": "午餐后",
            "measureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "unusual": 4,
            "comment": "zdh4"
        })
        return data

    def add_zy_glu5(self):  # 添加血糖

        data = json.dumps({
            "userId": read_zy_yaml()['userId'],
            "valueUnit": 1,
            "method": 0,
            "nurseId": read_yaml('userId'),
            "timeType": "晚餐前",
            "measureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "unusual": 5,
            "comment": "zdh5"
        })
        return data

    def add_zy_glu6(self):  # 添加血糖

        data = json.dumps({
            "userId": read_zy_yaml()['userId'],
            "valueUnit": 1,
            "method": 0,
            "nurseId": read_yaml('userId'),
            "timeType": "晚餐后",
            "measureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "unusual": 6,
            "comment": "zdh6"
        })
        return data

    def add_zy_glu7(self):  # 添加血糖

        data = json.dumps({
            "userId": read_zy_yaml()['userId'],
            "valueUnit": 1,
            "method": 0,
            "nurseId": read_yaml('userId'),
            "timeType": "随机",
            "measureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "unusual": 7,
            "comment": "zdh7"
        })
        return data

    def add_zy_glu8(self):  # 添加血糖

        data = json.dumps({
            "userId": read_zy_yaml()['userId'],
            "valueUnit": 1,
            "method": 0,
            "nurseId": read_yaml('userId'),
            "timeType": "q3h",
            "measureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "unusual": 8,
            "comment": "zdh8"
        })
        return data

    def add_zy_glu9(self):  # 添加血糖

        data = json.dumps({
            "userId": read_zy_yaml()['userId'],
            "valueUnit": 1,
            "method": 0,
            "nurseId": read_yaml('userId'),
            "timeType": "随机",
            "measureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "unusual": 9,
            "comment": "zdh9"
        })
        return data

    '''
    获取患者血糖测试用例
    '''

    def zy_patient_glu1(self):  # 获取患者血糖
        data = json.dumps({
            "userId": read_zy_yaml()['userId'],
            "pageNo": 1,
            "orderBy": "measure_time desc",
            "pageSize": 20,
            "patGluStatus": 1
        })
        return data

    def zy_patient_glu2(self):  # 获取患者血糖
        data = json.dumps({
            "userId": read_zy_yaml()['userId'],
            "pageNo": 1,
            "orderBy": "measure_time desc",
            "pageSize": 10,
            "patGluStatus": 2
        })
        return data

    def zy_patient_glu3(self):  # 获取患者血糖
        data = json.dumps({
            "userId": read_zy_yaml()['userId'],
            "pageNo": 1,
            "orderBy": "measure_time desc",
            "pageSize": 10,
            "patGluStatus": 3
        })
        return data

    def zy_patient_glu_report1(self):  # 获取患者血糖
        data = json.dumps({
            "userId": read_zy_yaml()['userId'],
            "pageNo": 1,
            "orderBy": "measure_time desc",
            "pageSize": 10,
            "patGluStatus": 1
        })
        return data

    def zy_patient_glu_report2(self):  # 获取患者血糖
        data = json.dumps({
            "userId": read_zy_yaml()['userId'],
            "pageNo": 1,
            "orderBy": "measure_time desc",
            "pageSize": 20,
            "patGluStatus": 2
        })
        return data

    def zy_patient_glu_report3(self):  # 获取患者血糖
        data = json.dumps({
            "userId": read_zy_yaml()['userId'],
            "pageNo": 1,
            "orderBy": "measure_time desc",
            "pageSize": 20,
            "patGluStatus": 3
        })
        return data

    '''
    患者血糖趋势图
    '''

    def patientTrendChart(self):  # 获取患者血糖
        data = json.dumps({
            "userId": read_zy_yaml()['userId'],
            "patGluStatus": 1})
        return data

    '''
    患者血糖统计图
    '''

    def patientPieChart(self):  # 血糖统计图
        data = json.dumps({
            "userId": read_zy_yaml()['userId'],
            "patGluStatus": 1})
        return data

    '''
    # 更新患者血糖测试用例，更新时段，更新血糖值
    # '''

    def zy_patient_glu_update1(self):  # 更新患者血糖时段
        data = json.dumps({
            "comment": "修改时段",
            "id": str(int(read_zy_blood_yaml()['id']) ),
            "measureTime": read_zy_blood_yaml()['measureTime'],
            "method": 0,
            "value": 5,
            "nurseId": read_yaml('userId'),
            "timeType": "q2h",
            "unusual": 1,
            "userId": read_zy_blood_yaml()["userId"],
            "valueUnit": 1,
        })
        return data

    def zy_patient_glu_update2(self):  # 更新患者血糖值
        data = json.dumps({
            "comment": "血糖值修改",
            "id": str(int(read_zy_blood_yaml()['id']) ),
            "measureTime": read_zy_blood_yaml()['measureTime'],
            "method": 0,
            "value": 8,
            "nurseId": read_yaml('userId'),
            "timeType": "早餐前",
            "unusual": 1,
            "userId": read_zy_yaml()["userId"],
            "valueUnit": 1,
        })
        return data

    '''
    删除血糖测试用例
    '''

    def zy_patient_glu_del0(self):  # 删除血糖
        data = json.dumps({
            "id": str(int(read_zy_blood_yaml()['id'])),

        })
        return data

