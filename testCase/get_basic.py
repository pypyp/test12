import json, yaml
from common.yaml_util import \
    read_mz_yaml, read_zy_yaml, read_csv, read_yaml
from data.read_fun import Load_Basic
import time,random

'''
此类用于获取在线门诊第一个患者的个人信息和第一条血糖数据
'''


class mz:
    def get_patient_info(self):
        data = json.dumps({"pageNo": 1, "pageSize": 21, "day": 1})
        return data

    def add_glu(self,userId):  # 添加血糖
        data = json.dumps({
            "userId": userId,
            "value": 6.2,
            "valueUnit": 1,
            "method": 0,
            "nurseId": read_yaml('userId'),
            "timeType": "q2h",
            "measureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "unusual": 2,
            'comment': '添加'
        })
        return data

    def get_blood_info(self,userId):
        data = json.dumps({
            "userId": userId,
            "pageNo": 1,
            "orderBy": "id desc",
            "pageSize": 20
        })
        return data


class zy():

    def get_patient_info(self):
        data = json.dumps({"pageNo": 1, "pageSize": 15})
        return data

    def add_glu(self, userId):  # 添加血糖

        data = json.dumps({
            "userId": userId,
            "value": 6.2,
            "valueUnit": 1,
            "method": 0,
            "nurseId": read_yaml('userId'),
            "timeType": "q2h",
            "measureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "unusual": 1,
            "comment": 'cs'
        })
        return data

    def get_blood_info(self, userId):
        data = json.dumps({
            # "userId": (read_zy_yaml()['userId']),
            "userId": userId,
            "pageNo": 1,
            "orderBy": "id desc",
            "pageSize": 20
        })
        return data

    def alarmlist(self):
        data = json.dumps({
            # "deptId": read_zy_yaml()['deptId'],
            "pageNo": 1,
            "pageSize": 20
        })

    def get_order(self):
        data = json.dumps({
            "pageNo": 1,
            "pageSize": 15,
            "endTime": time.strftime("%Y-%m-%d 23:59:59", time.localtime()),
            "startTime": time.strftime("%Y-%m-%d 00:00:00", time.localtime())
            # "deptId": read_zy_yaml()['deptId']
        })
        return data

    def add_order(self, userId):
        data = json.dumps({
            "userId": userId,
            "type": 0,
            "timeType": "q2h",
            "startTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "entrust": ""})
        return data


class zy_temp:
    def tmep_glu_list(self):  # 获取临时检测血糖列表
        data = json.dumps({
            "endtTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "startTime": time.strftime("%Y-%m-%d 00:00:00", time.localtime())

        })
        return data

    def add_glu(self):  # 添加血糖
        data = json.dumps({
            "value": 6.2,
            "valueUnit": 1,
            "method": 0,
            "nurseId": read_yaml('userId'),
            "timeType": "q2h",
            "measureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "unusual": 1
        })
        return data


class qc_record:
    def qc_add(self):
        value = 15.3
        liquid=random.choice(Load_Basic.read_liquid_info())
        paper=random.choice(Load_Basic.read_paper_info())
        sn=random.choice(Load_Basic.read_sn_info())
        if liquid['type'] == 0:
            if value < paper['lowMinLimit'] or value > paper['lowMaxLimit']:
                result = 1
            else:
                result = 0

        elif liquid['type'] == 1:
            if value < paper['mediumMinLimit'] or value > paper['mediumMaxLimit']:
                result = 1
            else:
                result = 0
        else:
            if value < paper['mediumMinLimit'] or value > paper['mediumMaxLimit']:
                result = 1
            else:
                result = 0
        data = {
            "value": value,
            "sn": sn['sn'],
            "liquidId": liquid['id'],
            'paperId': paper['id'],
            "measureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "result": result,
        }
        print(data
              )
        return data
