import os
import sys

sys.path.append(r'' + os.path.abspath('../'))
import json
from common.yaml_util import read_zy_blood_yaml, read_csv, read_zy_yaml, read_bastase_sql, read_yaml
from common.open_database import MysqlDb
import time


class zy_alarmlist:
    # def get_warn_info(id):
    # warn_info['id'] = id


    def glu_alarmList1(self):  # 血糖预警列表
        data = json.dumps({"pageNo": 1, "pageSize": 15})
        return data
    def glu_alarmList2(self):  # 血糖预警列表
        data = json.dumps({"pageNo": 1, "pageSize": 15,"alarmType":1})
        return data
    def glu_alarmList3(self):  # 血糖预警列表
        data = json.dumps({"pageNo": 1, "pageSize": 15,"alarmType":2})
        return data

    # def glu_warning_update():  # 修改血糖预警状态
    #
    #     data = json.dumps({"id": warn_info['id'], "warningStatus": 1})
    #     return data

    #
    # order_id = {}