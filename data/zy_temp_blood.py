# coding=UTF-8
import os
import sys

sys.path.append(r'' + os.path.abspath('../'))
import json
from common.yaml_util import read_zy_temp_yaml,read_csv,read_zy_yaml,read_bastase_sql,read_yaml
from common.open_database import MysqlDb
import time

class zy_temp_blood:

    '''
    添加血糖测试用例
    '''

    def add_zy_temp_glu0(self):  # 添加血糖
        data = json.dumps({
            # "userId": read_zy_yaml()['userId'],
            "value": 5,
            "valueUnit": 1,
            "method": 0,
            "nurseId": read_yaml('userId'),
            "timeType": "q2h",
            "measureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "unusual": 1,
            "comment": "手动添加"})
        return data

    def add_zy_temp_glu1(self):  # 添加血糖
        data = json.dumps({
            "userId": read_zy_yaml()['userId'],
            "value": 6.2,
            "valueUnit": 1,
            "method": 0,
            "nurseId": read_yaml('userId'),
            "timeType": "q2h",
            "measureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "unusual": 2,
            "comment": "绑定患者添加"})
        return data


    '''
    临时检测血糖列表
    '''
    def tmep_glu_list1(self):  # 获取临时检测血糖列表
        data = json.dumps({

            })
        return data

    def tmep_glu_list2(self):  # 获取临时检测血糖列表
        data = json.dumps({
            "endtTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "startTime": time.strftime("%Y-%m-%d 00:00:00", time.localtime())

        })
        return data

    '''
    # 临时检测血糖修改
    # '''
    def temp_glu_update0(self):  # 血糖修改
        data = json.dumps({
            "id": str(int(read_zy_temp_yaml()['id'])),
            'timeType': '早餐后'
            })
        return data

    def temp_glu_update1(self):  # 血糖修改
        data = json.dumps({
            "id": str(int(read_zy_temp_yaml()['id'])),
            'timeType': '早餐后',
            "userId": read_zy_yaml()['userId'],
            "comment":'添加'
            })
        return data

    '''
    临时检测删除血糖
    '''

    def temp_glu_del(self):  # 血糖删除

        data = json.dumps({
            "id": str(int(read_zy_temp_yaml()['id']) + 2)
        })
        return data
    #
    # '''
    # # 更新患者血糖测试用例，更新时段，更新血糖值
    # # '''
    # def zy_patient_glu_update1(self):  #更新患者血糖时段
    #     data = json.dumps({
    #             "comment": "测试",
    #             "id": str(int(read_zy_blood_yaml()['id'])+1),
    #             "measureTime": read_zy_blood_yaml()['measureTime'],
    #             "method": 0,
    #             "value": 6.2,
    #             "nurseId": read_csv()[0],
    #             "timeType": "q3h",
    #             "unusual": 2,
    #             "userId": read_zy_blood_yaml()["userId"],
    #             "valueUnit": 1,
    #         })
    #     return data
    #
    # def zy_patient_glu_update2(self):  #更新患者血糖值
    #     data = json.dumps({
    #             "comment": "测试",
    #             "id": str(int(read_zy_blood_yaml()['id'])+2),
    #             "measureTime": read_zy_blood_yaml()['measureTime'],
    #             "method": 0,
    #             "value": 6.6,
    #             "nurseId": read_csv()[0],
    #             "timeType": "q3h",
    #             "unusual": 2,
    #             "userId": read_zy_yaml()["userId"],
    #             "valueUnit": 1,
    #         })
    #     return data
    #
    # '''
    # 删除血糖测试用例
    # '''
    # def zy_patient_glu_del0(self):  #删除血糖
    #     data = json.dumps({
    #             "id": str(int(read_zy_blood_yaml()['id'])+1),
    #
    #         })
    #     return data
    #
    # def zy_patient_glu_del1(self):  #删除血糖
    #     data = json.dumps({
    #             "id": str(int(read_zy_blood_yaml()['id'])+2),
    #
    #         })
    #     return data