# coding=UTF-8
import sys
import os
sys.path.append(r''+os.path.abspath('../'))
import json
import time
from common.yaml_util import read_mz_yaml,read_bastase_sql
from common.com import Ran
from common.open_database import MysqlDb
time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


class mz_patient:
    '''
    获取门诊患者血糖用例，获取所有，今日，历史
    '''

    def in_patient_0(self):  # 今日门诊患者
        data = json.dumps({"pageNo": 1, "pageSize": 15, "day":1})
        return data

    def in_patient_1(self):  # 历史门诊患者
        data = json.dumps({"pageNo": 1, "pageSize": 15, "day": 2})
        return data

    def in_patient_2(self):  # 所有门诊患者
        data = json.dumps({"pageNo": 1, "pageSize": 15})
        return data

    '''
    获取患者基本信息测试用例
    '''
    def patient_info(self):  # 获取患者基本信息
        data = json.dumps({"userId": read_mz_yaml()['userId']})
        return data

    '''
    获取患者所有门诊记录
    '''
    def patient_listRecord(self):  # 获取患者所有门诊记录
        data = json.dumps({"userId": read_mz_yaml()['userId'],
                           "pageNo": 1,
                           "pageSize": 20
                           })
        return data
    '''
    更新患者基本信息，更新手机号
    '''
    def patient_info_update1(self):  # 更新患者基本信息
        data = json.dumps({
                'userId':read_mz_yaml()['userId'],
                "name": read_mz_yaml()["name"],
                "gender": read_mz_yaml()["gender"],
                "birthday": read_mz_yaml()["birthday"],
                "primayDocId": read_mz_yaml()["primayDocId"],
                "deptId": read_mz_yaml()["deptId"],
                "idCard": read_mz_yaml()["idCard"],
                "phone": Ran().phoneNORandomGenerator(),
                'mzDate':read_mz_yaml()['mzDate']
        })
        return data

    def patient_info_add0(self):  # 添加患者
        data = json.dumps({
                "name": Ran().number(),
                "gender": read_mz_yaml()["gender"],
                "birthday": read_mz_yaml()["birthday"],
                "primayDocId": read_mz_yaml()["primayDocId"],
                "deptId": read_mz_yaml()["deptId"],
                "idCard": Ran().ran_end(),
                "phone": Ran().phoneNORandomGenerator(),
                'mzDate':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        })
        return data


    def patient_register(self):  # 历史门诊登记
        data0 = MysqlDb().select_db(
            "SELECT * FROM {}.`mz_patient` WHERE user_id = "
            "(SELECT user_id FROM {}.`mz_record` WHERE TO_DAYS(mz_date) < TO_DAYS(NOW()) ORDER BY mz_date desc limit 1)".

            format(
                read_bastase_sql()[4],
                read_bastase_sql()[4]
                ))

        data = json.dumps({
                'userId':data0[0]['user_id'],
                "name": data0[0]["name"],
                "gender": data0[0]["gender"],
                "birthday": data0[0]["birthday"],
                "primayDocId": data0[0]["primayDocId"],
                "deptId": data0[0]["deptId"],
                "idCard": data0[0]["idCard"],
                "phone": data0[0]["phone"],
                'mzDate': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        })
        return data