# coding=UTF-8
import sys
import os
sys.path.append(r''+os.path.abspath('../../'))
import json
import time
import datetime
from random import random
import random

time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def getheader():
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "Accept": "application/json, text/plain, */*",
        "Project": "vivachekcloud",
        "Platform": "3",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/89.0.4389.114 Safari/537.36",
        "Version": "v1.7.0",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "h-CN,zh;q=0.9",
        "Connection": "keep-alive"
    }
    return headers


def login():  # 用户登陆
    data = json.dumps({"hisId": "vivachek", "password": "123456"})
    return data


def in_patient():  # 获取住院患者
    data = json.dumps({"pageNo": 1, "pageSize": 15})
    return data


def patient_count():  # 患者统计
    data = json.dumps({"pageNo": 1, "pageSize": 15})
    return data


def out_patient():  # 获取出院患者
    data = json.dumps({"pageNo": 1, "pageSize": 15})
    return data


info = {}  # 存放信息


def get_userid(userid, outuserid, iptNum, name, deptId, deptName):
    info['userid'] = userid
    info['outuserid'] = outuserid
    info['iptNum'] = iptNum
    info['name'] = name
    info['deptId'] = deptId
    info['deptName'] = deptName


def healthArchives():  # 获取控糖目标
    data = json.dumps({"userId": info['userid']})
    return data


def patient_info():  # 获取患者基本信息
    data = json.dumps({"userId": info['userid']})
    return data


def update_patient_info():  # 更新患者基本信息
    data = json.dumps({"birthday": "2020-11-04",
                       "deptId": info['deptId'],
                       "gender": 1,
                       "iptNum": info['iptNum'],
                       "iptTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                       "name": info['name'],
                       "status": 1,
                       "userId": info['userid']})
    return data


def add_patient():  # 添加患者
    data = json.dumps({
        "name": random.choice('abcdefghijklmnopqrstuvwxyz!@#$%^&*()'),
        "gender": 2,
        "birthday": "2021-07-06",
        "iptNum": str(random.randint(0, 500)),
        "deptId": info['deptId'],
        "deptName": info['deptName'],
        "iptTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    })
    return data


def change_bed():  # 换床
    data = json.dumps({"userId": info['userid'], "bedNum": "+52"})
    return data


def change_dept():  # 转科
    data = json.dumps({"deptId": "60",
                       "deptName": "外科",
                       "userId": info['userid']})
    return data


def out_hospital():  # 患者出院
    data = json.dumps({"userId": info['outuserid']})
    return data


def transfers():  # 转诊
    pass


def transfers_info():  # 转诊详情
    pass


def add_glu():  # 添加血糖
    data = json.dumps({
        "userId": info['userid'],
        "value": 6.2,
        "valueUnit": 1,
        "method": 0,
        "nurseId": "vivachek",
        "timeType": "q2h",
        "measureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "unusual": 1,
        "comment": "测试"})
    return data


glu_id = {}


def get_glu_id(id):
    glu_id['id'] = id


def patient_glu_list():  # 患者血糖列表
    data = json.dumps({
        "userId": info['userid'],
        "startTime": (datetime.datetime.now() + datetime.timedelta(days=-15)).strftime("%Y-%m-%d %H:%M:%S"),
        "endTime": (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
        "pageNo": 1,
        "pageSize": 20})
    return data


def patient_glu_report():  # 患者血糖报告
    data = json.dumps({
        "userId": info['userid'],
        # "startTime": (datetime.datetime.now() + datetime.timedelta(days=-15)).strftime("%Y-%m-%d %H:%M:%S"),
        # "endTime": (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
        "pageNo": 1,
        "pageSize": 20})
    return data


def update_glu():  # 修改血糖
    data = json.dumps({
        "comment": "测试",
        "id": glu_id['id'],
        "measureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "method": 0,
        "nurseId": "vivachek",
        "paperNum": 1,
        "timeType": "q2h",
        "unusual": 4,
        "userId": info['userid'],
        "valueUnit": 1})
    return data


def del_glu():  # 删除血糖
    data = json.dumps({"id": glu_id['id']})
    return data


def glu_info():  # 血糖详情
    data = json.dumps({"id": glu_id['id']})
    return data


def patientTrendChart():  # 患者趋势图
    data = json.dumps({
        "userId": info['userid'],
        "startTime": (datetime.datetime.now() + datetime.timedelta(days=-15)).strftime("%Y-%m-%d %H:%M:%S"),
        "endTime": (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
        "patGluStatus": 1})
    return data


def patientPieChart():  # 血糖统计图
    data = json.dumps({
        "userId": info['userid'],
        "startTime": (datetime.datetime.now() + datetime.timedelta(days=-15)).strftime("%Y-%m-%d %H:%M:%S"),
        "endTime": (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
        "patGluStatus": 1})
    return data


warn_info = {}


def get_warn_info(id):
    warn_info['id'] = id


def glu_alarmList():  # 血糖预警列表
    data = json.dumps({"pageNo": 1, "pageSize": 15})
    return data


def glu_warning_update():  # 修改血糖预警状态

    data = json.dumps({"id": warn_info['id'], "warningStatus": 1})
    return data


order_id = {}


def get_order_id(id):
    order_id['id'] = id


def add_glu_order():  # 添加任务
    data = json.dumps({
        "userId": info['userid'],
        "type": 0,
        "timeType": "q2h",
        "startTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "entrust": ""
    })

    return data


def glu_order_getPatientOrderList():  # 患者任务列表
    data = json.dumps({"userId": info['userid']})
    return data


def update_glu_order():  # 编辑任务
    data = json.dumps({
        "id": order_id['id'],
        "userId": info['userid'],
        "type": 0,
        "timeType": "q2h",
        "startTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "entrust": "按时"
    })
    print(info['userid'])
    return data


def glu_order_info():  # 任务详情
    data = json.dumps({
        "id": order_id['id'],
    })
    return data


def stop_glu_info():  # 停止任务
    data = json.dumps({
        "id": order_id['id'] + 1,
    })
    return data


# def glu_order_monitorList():  # 停止今日任务app
#     data = json.dumps({
#         "id": 16211,
#     })
#     return data


# def glu_order_addMeasure():  # 添加检测 app
#     data = json.dumps({
#         "id": 16216,
#         "userId": "100000006",
#         "nurseId": "437302807603707904",
#         "unusual": 1,
#         "method": 1,
#         "timeType": "午餐后",
#         "measureTime": "2021-07-07 15:40:58",
#         "value": 40.0,
#         "valueUnit": 1,
#         "paperNum": 1,
#         "deviceNo": "359B000035A"
#     })
#     return data


def glu_order_web_monitorList():  # 检测任务列表
    data = json.dumps({"pageNo": 1, "pageSize": 15})
    return data


def glu_app_measureGluList():  # app院内检测
    data = json.dumps({
        "viewType": 1,
        "pageNo": 1,
        "pageSize": 10
    })
    return data


ls = {}


def get_ls_id(id):
    ls['id'] = id


def measure_temp_add():  # 临时检测添加血糖
    data = json.dumps({

        "value": 5.2,
        "valueUnit": 1,
        "method": 0,
        "nurseId": "vivachek",
        "timeType": "午餐后",
        "measureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "unusual": 1,
        "comment": "测试"
    })
    return data


def measure_temp_update():  # 临时检测修改血糖
    data = json.dumps({

        "id": ls['id'],
        "timeType": "qd",

    })
    return data


def measure_temp_info():  # 临时检测血糖详情
    data = json.dumps({

        "id": ls['id'],

    })
    return data


def measure_temp_delete():  # 临时检测删除血糖
    data = json.dumps({

        "id": ls['id'],

    })
    return data


def measure_temp_uploadMeasures():  # 上传离线临时检测
    data = json.dumps({

        "measures": [{
            "value": 6.3,
            "valueUnit": 1,
            "method": 0,
            "nurseId": "vivachek",
            "timeType": "早餐后",
            "measureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "unusual": 1,
            "comment": "测试",
            "status": 1
        }
        ]
    })
    return data


def measure_temp_list():  # 临时检测记录
    data = json.dumps({
        "startTime": (datetime.datetime.now() + datetime.timedelta(days=-15)).strftime("%Y-%m-%d %H:%M:%S"),
        "endTime": (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
    })
    return data


def device_add():  # 添加设备
    data = json.dumps({
        "bindModule": 0,
        "contrastTest": 0,
        "devQuality": 0,
        "devStatus": 0,
        "enableAdb": 1,
        "enableMtk": 0,
        "enableTouchFeedback": 0,
        "externalQuality": 0,
        "inhosDeptId": "3",
        "sn": "359B0000357",
        "uploadMtk": 0
    })

    return data


def device_update():  # 编辑设备
    pass


def device_del():  # 删除设备
    pass


def device_info():  # 查询设备
    pass


paper = {}


def get_paper(id):
    paper['id'] = id


def paper_add():  # 添加试纸
    data = json.dumps({
        "specs": 0,
        "paperNum": 20,
        "productionDate": "2018-09-01",
        "expiryDate": "2022-09-01",
        "lowMaxLimit": "50",
        "lowMinLimit": "2",
        "mediumMaxLimit": "40",
        "mediumMinLimit": "3",
        "highMaxLimit": "30",
        "highMinLimit": "6",
        "batchNum": "2019020231"
    })
    return data


def paper_update():  # 修改试纸信息
    data = json.dumps({

        "id": paper['id'],
        "specs": 0,
        "paperNum": 20,
        "productionDate": "2018-09-01",
        "expiryDate": "2022-09-01",
        "lowMaxLimit": "9",
        "lowMinLimit": "2",
        "mediumMaxLimit": "15",
        "mediumMinLimit": "9",
        "highMaxLimit": "30",
        "highMinLimit": "15",
        "batchNum": "2019020231"
    })
    return data


def paper_del():  # 删除试纸
    data = json.dumps({
        "id": paper['id']
    })
    return data


def paper_info():  # 查询试纸
    data = json.dumps({
        "pageNo": 1,
        "pageSize": 20
    })
    return data


liqiuid = {}


def get_liquid(id):
    liqiuid['id'] = id


def liquid_add():  # 添加质控液
    data = json.dumps({
        "specs": 0,
        "liquidNum": 20,
        "type": 0,
        "productionDate": "2018-09-01",
        "expiryDate": "2022-09-01",
        "batchNum": "2019020231"
    })
    return data


def liquid_update():  # 修改质控液
    data = json.dumps({
        "id": liqiuid['id'],
        "specs": 0,
        "liquidNum": 20,
        "type": 1,
        "productionDate": "2018-09-01",
        "expiryDate": "2022-09-01",
        "batchNum": "2019020231"
    })
    return data


def liquid_del():  # 删除质控液
    data = json.dumps({
        "id": liqiuid['id']
    })
    return data


def liquid_info():  # 查询质控液
    data = json.dumps({
        "pageNo": 1,
        "pageSize": 20
    })
    return data


def qc_record_list():  # 质控查询
    data = json.dumps({"pageNo": 1, "pageSize": 15})
    return data


def qc_record_add():  # 质控添加
    data = json.dumps({
        "value": 15.3,
        "sn": "359B00000D9",
        "measureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "paperId": 35,
        "liquidId": 2,
        "liquidOpenTime": time.strftime("%Y-%m-%d", time.localtime()),
        "paperOpenTime": time.strftime("%Y-%m-%d", time.localtime()),
        "result": 1,
        "paperNum": 1
    })
    return data


def qc_record_update():  # 修改质控
    data = json.dumps({
        "id": 538,
        "liquidId": 41,
        "measureTime": "2021-06-21 14:40:00",
        "paperId": 32,
        "result": 0,
        "sn": "359B0000064",
        "value": 8.6
    })
    return data


def qc_record_del():  # 删除质控
    data = json.dumps({
        "id": 538,

    })
    return data


def qc_record_analysis():  # 质控分析列表
    data = json.dumps({

    })
    return data


def qc_record_statistics():  # 质控统计列表
    data = json.dumps({
        "pageNo": 1,
        "pageSize": 20
    })
    return data


def cp_manage_list():  # 对比管理列表
    data = json.dumps({
        "pageNo": 1,
        "pageSize": 20
    })
    return data


qc_record = {}


def get_qc_record(id, sn, batchNum, sampleNum):
    qc_record['id'] = id
    qc_record['sn'] = sn
    qc_record['batchNum'] = batchNum
    qc_record['sampleNum'] = sampleNum


def qc_record_external_list():  # web室间质评列表
    data = json.dumps({
        "pageNo": 1,
        "pageSize": 20
    })
    return data


def qc_record_external_add():  # 添加室间质评
    data = json.dumps({

        "batchNum": qc_record['batchNum'],
        "measureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "nurseId": "vivachek",
        "sampleNum": 'cds',
        "sn": qc_record['sn'],
        "value": 2

    })
    return data


def qc_record_external_update():  # 修改室间质评
    data = json.dumps({
        "batchNum": qc_record['batchNum'],
        "id": qc_record['id'],
        "measureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "nurseId": "vivachek",
        "sampleNum": "B",
        "sn": qc_record['sn'],
        "value": 9
    })
    return data


def qc_record_external_del():  # 删除室间质评
    data = json.dumps({
        "id": qc_record['id'],
    })
    return data


def qc_record_external_app():  # app室间质评列表
    data = json.dumps({
        "sn": "359B000049C"
    })
    return data
