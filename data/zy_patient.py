import sys
import os
sys.path.append(r''+os.path.abspath('../'))
import json
import time
from common.yaml_util import read_zy_yaml,read_bastase_sql
from testCase.log import logger
from common.com import Ran
from common.open_database import MysqlDb
class zy:

    '''
    住院患者测试用例,所有权限，科室筛选，床号筛选，住院号,姓名筛选
    '''
    def in_patient_0(self):  # 获取所有权限下得住院患者
        data = json.dumps({"pageNo": 1, "pageSize": 15})
        return data

    def in_patient_1(self):  # 筛选科室住院患者
        data = json.dumps({"pageNo": 1, "pageSize": 15, 'deptId':read_zy_yaml()['deptId']})
        return data

    def in_patient_2(self):  # 筛选床号住院患者
        data = json.dumps({"pageNo": 1, "pageSize": 15, 'bedNum':'08'})
        return data

    def in_patient_3(self):  # 筛选住院号住院患者
        data = json.dumps({"pageNo": 1, "pageSize": 15, 'iptNum':read_zy_yaml()['iptNum']})
        return data

    def in_patient_4(self):  # 筛选姓名住院患者
        data = json.dumps({"pageNo": 1, "pageSize": 15, 'iptNum':read_zy_yaml()['name']})
        return data

    '''
    出院患者测试用例，所有，根据科室，住院号，姓名筛选
    '''

    def out_patient_0(self):  # 获取所有权限下得出院患者
        data = json.dumps({"pageNo": 1, "pageSize": 15})
        return data

    def out_patient_1(self):  # 筛选科室出院患者
        data = json.dumps({"pageNo": 1, "pageSize": 15, 'deptId':read_zy_yaml()['deptId']})
        return data

    def out_patient_2(self):  # 筛选住院号出院患者
        data = json.dumps({"pageNo": 1, "pageSize": 15, 'iptNum':read_zy_yaml()['iptNum']})
        return data

    def out_patient_3(self):  # 筛选名字出院患者
        data = json.dumps({"pageNo": 1, "pageSize": 15, 'name': "测试"})
        return data

    '''
    患者详情根据userid或者住院号
    '''
    def patient_info_0(self):  # 筛选名字出院患者
        data = json.dumps({'userId': read_zy_yaml()['userId']})
        return data

    def patient_info_1(self):  # 筛选名字出院患者
        data = json.dumps({'iptNum': read_zy_yaml()['iptNum']})
        return data

    '''
    获取控糖目标
    '''
    def healthArchives(self):  # 筛选名字出院患者
        data = json.dumps({'userId': read_zy_yaml()['userId']})
        return data

    '''
    更新患者信息，修改手机号，修改床号，
    '''
    def update_patient_info_1(self):  # 修改手机号
        data = json.dumps({"birthday": read_zy_yaml()['birthday'],
                           "deptId": read_zy_yaml()['deptId'],
                           "gender": 1,
                           "iptNum": read_zy_yaml()['iptNum'],
                           "iptTime": read_zy_yaml()['iptTime'],
                           "name": read_zy_yaml()['name'],
                           "status": 1,
                           "userId": read_zy_yaml()['userId'],
                           'bedNum': '44',
                           'phone':Ran().phoneNORandomGenerator()})

        return data

    def update_patient_info_2(self):  # 修改床号
        data = json.dumps({"birthday": read_zy_yaml()['birthday'],
                           "deptId": read_zy_yaml()['deptId'],
                           "gender": 1,
                           "iptNum": read_zy_yaml()['iptNum'],
                           "iptTime": read_zy_yaml()['iptTime'],
                           "name": read_zy_yaml()['name'],
                           "status": 1,
                           "userId": read_zy_yaml()['userId'],
                           'bedNum':Ran().number(),
                           'phone':''})

        return data


    '''
    换床
    '''
    def change_bed0(self):  # 换床
        data = json.dumps({
                            "userId": read_zy_yaml()['userId'],
                            'bedNum':Ran().number()})

        return data

    def change_bed1(self):  # 换床
        data = json.dumps({
                            "userId": read_zy_yaml()['userId'],
                            'bedNum':"+1"})

        return data
    '''
    患者出院
    '''
    def out_hospital(self):  # 换床
        data = json.dumps({
                            "userId": read_zy_yaml()['userId'],
                            })

        return data
    '''
    扫码患者读取数据库权限配置
    '''

    def scan(self):  # 更新患者基本信息
        a = MysqlDb().select_db('SELECT code_base FROM {}.`print_template`'.format(read_bastase_sql()[4]))
        logger.getlogger().info('SELECT code_base FROM {}.`print_template`'.format(read_bastase_sql()[4]))
        if str(a[0]['code_base']) == '1': #扫住院
            data = json.dumps({
                "scanCode": read_zy_yaml()['iptNum'],
                })
            return data

        if str(a[0]['code_base']) == '2': #扫床号
            try:
                read_zy_yaml()['bedNum']
            except AssertionError:
                data = json.dumps({
                    "scanCode": read_zy_yaml()['deptId']
                    })
                return data
            data = json.dumps({
                "scanCode": read_zy_yaml()['deptId']+read_zy_yaml()['bedNum']
            })
            return data


    '''
    患者登记
    '''

    def add_patient(self):  # 添加患者
        data = json.dumps({
            "name": 'CS',
            "gender": 2,
            "birthday": time.strftime("%Y-%m-%d", time.localtime()),
            "iptNum": Ran().number(),
            "deptId": read_zy_yaml()['deptId'],
            "deptName": read_zy_yaml()['deptName'],
            "iptTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        })
        return data

