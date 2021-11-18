# coding=UTF-8
import os
import sys

sys.path.append(r'' + os.path.abspath('../'))
import json
from common.yaml_util import read_order_yaml,read_csv,read_zy_yaml,read_bastase_sql,read_yaml
from common.open_database import MysqlDb
import time

class zy_web_order:

    def add_order_glu(self):  # 添加血糖
        data = json.dumps({
            'id':read_order_yaml()['id'],
            "userId": read_zy_yaml()['userId'],
            "value": 5,
            "valueUnit": 1,
            "method": 0,
            "nurseId": read_yaml('userId'),
            "timeType": read_order_yaml()['timeType'],
            "measureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "unusual": 1,
            "comment": "zdh0"
        })
        return data

    def glu_order_getPatientOrderList(self):
        data = json.dumps({"userId": read_order_yaml()['userId']})
        return data

    def glu_order_info(self):  # 任务详情
        data = json.dumps({
            "id": read_order_yaml()['id'],
        })
        return data

    def update_glu_order(self):  # 编辑任务
        data = MysqlDb().select_db(
            "select * from {}.`medical_order_detail`where id=\'{}\' ".format(read_bastase_sql()[4],
                                                                             read_order_yaml()[
                                                                                 'id']))
        data = json.dumps({
            "id": data[0]['order_id'],
            "userId": read_order_yaml()['userId'],
            "type": 0,
            "timeType": "随机",
            "startTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "entrust": "zdh"
        })
        return data

    def stop_glu_info(self):  # 停止任务
        data = MysqlDb().select_db(
            "select * from {}.`medical_order`order by id desc ".format(read_bastase_sql()[4],
                                                                       ))
        data1 = json.dumps({
            "id": data[0]['id'],
        })
        return data1