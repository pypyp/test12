import threading
import time, sqlite3
from testCase.offline_basic import basic
from common.yaml_util import read_url_csv, read_csv
import json, requests
from data import offline_glu
from testCase.offline_basic.sqlite import sqlite
import pytest

headers = {
    "Content-Type": "application/json;charset=UTF-8",
    "Accept": "application/json, text/plain, */*",
    "Project": "vivachekcloud",
    "Platform": "1",
    "Version": "v1.7.0",
    "X-User-Agent": "t9801/30",
    "Connection": "keep-alive",
    'Sn': "359A00004C2",
    'Offline': '1',
    'TimeStampReq': basic.get_unixtime(),
    'Nonce': basic.get_Nonce()
}

offline = {
    "deptUpdateTime": "",
    "staffUpdateTime": "",
    "patientUpdateTime": "",
    "gluUpdateTime": "",
    "measureUpdateTime": "",
    "liquidAndPaperUpdateTime": "",
    "qcRecordUpdateTime": "",
    "comparisonUpdateTime": "",
    "healthArchivesUpdateTime": "",
    "mzPatUpdateTime": "",
    "mzGluUpdateTime": "",
    "externalUpdateTime": "",
    "userIds": "",
    "offlineDataAuth": ""

}
url = read_url_csv()[1]

dict = {}


def before_login():
    print('------------首次离线数据开始------------')
    basc = requests.post(url.format('offline/system/print/info'), headers=headers, data=
    json.dumps({
        "pageNo": -1,
        "pageSize": 20
    })).json()
    response1 = requests.post(url.format('offline/getSynInfo'), headers=headers, data=json.dumps({})).json()
    time = response1['data']['systemTime']
    sql = """select count(*) from common_update_time"""
    if sqlite().select_id(sql)[0][0] == 0:
        sql = """INSERT INTO "common_update_time"("id", "deptUpdateTime", "staffUpdateTime", "patientUpdateTime", "gluUpdateTime", "measureUpdateTime", "qcUpdateTime", "deviceDeptId", "offlineDataAuth", "liquidAndPaperUpdateTime", "compareComparisonUpdateTime", "healthArchivesUpdateTime", "externalUpdateTime") 
        VALUES (1, '', '', '', '', '', '', \'{}\', \'{}\', '', '', '', '')""".format(response1['data']['deviceDeptId'],
                                                                                     response1['data'][
                                                                                         'offlineDataAuth'])
        sqlite().insert(sql)

        if response1['data']['deptUpdated'] == 1:
            pytest.main(["-sv", './test_offline/test_offline_dept.py'])
            sql = """UPDATE common_update_time SET deptUpdateTime = \'{}\' WHERE id =1
                                                                              """.format(time)
            sqlite().sqlite_update_time(sql)
        if response1['data']['staffUpdated'] == 1:
            pytest.main(["-sv", './test_offline/test_offline_common_staff_list.py'])
            sql = """UPDATE common_update_time SET staffUpdateTime = \'{}\' WHERE id =1
                                                                              """.format(time)
            sqlite().sqlite_update_time(sql)
        if response1['data']['liquidAndPaperUpdated'] == 1:
            pytest.main(["-sv", './test_offline/test_offline_paper_liquid.py'])

            sql = """UPDATE common_update_time SET liquidAndPaperUpdateTime = \'{}\' WHERE id =1
                                                              """.format(time)
            sqlite().sqlite_update_time(sql)
        if response1['data']['patientUpdated'] == 1:
            pytest.main(["-sv", './test_offline/test_offline_patient.py'])
            sql = """UPDATE common_update_time SET patientUpdateTime = \'{}\' WHERE id =1
                                                                      """.format(time)
            sqlite().sqlite_update_time(sql)
        if response1['data']['measureUpdated'] == 1:
            if basc['data']['hosId'] == 3:
                pytest.main(["-sv", './test_offline/test_offline_task.py::Test_offline_task::test_offline_task_0'])
                sql = """UPDATE common_update_time SET measureUpdateTime = \'{}\' WHERE id =1
                                                                                  """.format(time)
                sqlite().sqlite_update_time(sql)
            if basc['data']['hosId'] == 1:
                pytest.main(["-sv", './test_offline/test_offline_task.py::Test_offline_task::test_offline_task1'])
                sql = """UPDATE common_update_time SET measureUpdateTime = \'{}\' WHERE id =1
                                                                                              """.format(time)
                sqlite().sqlite_update_time(sql)
        if response1['data']['gluUpdated'] == 1:
            pytest.main(["-sv", './test_offline/test_offline_glu.py::Test_offline_glu_2'])
            sql = """UPDATE common_update_time SET gluUpdateTime = \'{}\' WHERE id =1
                                                                                          """.format(time)
            sqlite().sqlite_update_time(sql)
        if response1['data']['qcRecordUpdated'] == 1:
            pytest.main(["-sv", './test_offline/test_offline_qc.py::Test_offline_qc_2'])
            sql = """UPDATE common_update_time SET qcUpdateTime = \'{}\' WHERE id =1
                                                                                                  """.format(time)
            sqlite().sqlite_update_time(sql)
        if response1['data']['comparisonUpdated'] == 1:
            pytest.main(["-sv", './test_offline/test_offline_compare.py::Test_offline_compare::test_offline_compare_list'])
            sql = """UPDATE common_update_time SET compareComparisonUpdateTime = \'{}\' WHERE id =1
                                                                                                  """.format(time)
            sqlite().sqlite_update_time(sql)
        if response1['data']['externalUpdated'] == 1:
            pytest.main(
                ["-sv", './test_offline/test_offline_external.py::Test_offline_external::test_offline_external_list'])
            sql = """UPDATE common_update_time SET externalUpdateTime = \'{}\' WHERE id =1
                                                                                                          """.format(time)
            sqlite().sqlite_update_time(sql)

    print('------------首次离线数据结束------------')
def get_time():
    userid = sqlite().select_gloucose_islogin('select * from user where isLogin = 1')
    # sqlite().sqlite_update_time('update user set dataAuthIds=\'{}\' where isLogin = 1'.format('3'))

    auth = sqlite().select_gloucose_islogin('select dataAuthIds from user where isLogin = 1')
    sql = 'select deviceDeptId from common_update_time'
    dev = sqlite().select_id(sql)

    l = []
    for i in userid:
        l.append(i[0])
    l1 = []
    for i in auth:
        if i[0] in l1:
            pass
        else:
            l1.append(i[0])
    if dev[0][0] in l1:
        pass
    else:
        l1.append(dev[0][0])
    try:
        deptUpdateTime = sqlite().select_offline_time()[1]
    except:
        deptUpdateTime = ''
    try:
        staffUpdateTime = sqlite().select_offline_time()[2]
    except:
        staffUpdateTime = ''
    try:
        patientUpdateTime = sqlite().select_offline_time()[3]
    except:
        patientUpdateTime = ''
    try:
        gluUpdateTime = sqlite().select_offline_time()[4]
    except:
        gluUpdateTime = ''
    try:
        measureUpdateTime = sqlite().select_offline_time()[5]
    except:
        measureUpdateTime = ''
    try:
        qcRecordUpdateTime = sqlite().select_offline_time()[6]
    except:
        qcRecordUpdateTime = ''

    try:
        liquidAndPaperUpdateTime = sqlite().select_offline_time()[9]
    except:
        liquidAndPaperUpdateTime = ''

    try:
        comparisonUpdateTime = sqlite().select_offline_time()[10]
    except:
        comparisonUpdateTime = ''

    try:
        healthArchivesUpdateTime = sqlite().select_offline_time()[11]
    except:
        healthArchivesUpdateTime = ''

    try:
        externalUpdateTime = sqlite().select_offline_time()[11]
    except:
        externalUpdateTime = ''

    offline['deptUpdateTime'] = deptUpdateTime
    offline['staffUpdateTime'] = staffUpdateTime
    offline['patientUpdateTime'] = patientUpdateTime
    offline['gluUpdateTime'] = gluUpdateTime
    offline['measureUpdateTime'] = measureUpdateTime
    offline['qcRecordUpdateTime'] = qcRecordUpdateTime
    # offline['deviceDeptId'] = basic.sqlite().sqlite_update()[7]
    offline['offlineDataAuth'] = ",".join(l1)
    offline['liquidAndPaperUpdateTime'] = liquidAndPaperUpdateTime
    offline['comparisonUpdateTime'] = comparisonUpdateTime
    offline['healthArchivesUpdateTime'] = healthArchivesUpdateTime
    offline['externalUpdateTime'] = externalUpdateTime
    offline['userIds'] = l

    return offline

def DownloadAndUpload(time1):
    if '患者管理' in dict["permissions"]:
        if offline_glu.glu_upload()['measures'] != []:
            pytest.main(["-sv", './test_offline/test_offline_glu.py::Test_offline_glu_1'])
            sql = """UPDATE common_update_time SET gluUpdateTime = \'{}\' WHERE id =1""".format(time1)
            sqlite().sqlite_update_time(sql)
    if '设备管理' in dict["permissions"]:
        if offline_glu.qc_upload() != []:
            pytest.main(["-sv", './test_offline/test_offline_qc.py::Test_offline_qc_1'])
            sql = """UPDATE common_update_time SET qcUpdateTime = \'{}\' WHERE id =1
                                                                                                                     """.format(
                time1)
            sqlite().sqlite_update_time(sql)
    if offline_glu.external_upload() != []:
        pytest.main(["-sv", './test_offline/test_offline_external.py'])
        sql = """UPDATE common_update_time SET externalUpdateTime = \'{}\' WHERE id =1                                                                                                    """.format(
            time1)
        sqlite().sqlite_update_time(sql)
    if offline_glu.compare_upload() != []:
        pytest.main(["-sv", './test_offline/test_offline_compare.py'])
        sql = """UPDATE common_update_time SET compareComparisonUpdateTime = \'{}\' WHERE id =1
                                                                                                         """.format(
            time1)
        sqlite().sqlite_update_time(sql)

    response = requests.post(url.format('offline/getSynInfo'), headers=headers, data=json.dumps(get_time())).json()
    print(response)
    time = response['data']['systemTime']
    if response['data']['measureUpdated'] == 1:
        if dict['analysisModel'] == 0:
            pytest.main(["-sv", './test_offline/test_offline_task.py::Test_offline_task::test_offline_task_0'])
            sql = """UPDATE common_update_time SET measureUpdateTime = \'{}\' WHERE id =1
                                                                                                      """.format(time)
            sqlite().sqlite_update_time(sql)
        if dict['analysisModel'] == 1:
            pytest.main(["-sv", './test_offline/test_offline_task.py::Test_offline_task::test_offline_task_1'])
            sql = """UPDATE common_update_time SET measureUpdateTime = \'{}\' WHERE id =1
                                                                                                      """.format(time)
            sqlite().sqlite_update_time(sql)

    if response['data']['patientUpdated'] == 1:
        pytest.main(["-sv", './test_offline/test_offline_patient.py'])
        sql = """UPDATE common_update_time SET patientUpdateTime = \'{}\' WHERE id =1
                                                                          """.format(time)
        sqlite().sqlite_update_time(sql)

    if response['data']['gluUpdated'] == 1:
        pytest.main(["-sv", './test_offline/test_offline_glu.py::Test_offline_glu_1::test_offline_glu_list'])
        sql = """UPDATE common_update_time SET gluUpdateTime = \'{}\' WHERE id =1
                                                                                              """.format(time)
        sqlite().sqlite_update_time(sql)
    if response['data']['qcRecordUpdated'] == 1:
        pytest.main(["-sv", './test_offline/test_offline_qc.py::Test_offline_qc_1::test_offline_qc_list'])
        sql = """UPDATE common_update_time SET qcUpdateTime = \'{}\' WHERE id =1
                                                                                                      """.format(time)
        sqlite().sqlite_update_time(sql)

def login():
    global dict

    response = requests.post(url.format('login'), headers=headers, data=json.dumps({"hisId": read_csv()[0],
                                                                                    "password": read_csv()[1],
                                                                                    'sn': '359A00004C2'}))
    sql = """UPDATE user SET accessToken = \'{}\', refreshToken = \'{}\',isLogin=\'{}\',lastLoginTime = \'{}\'
    WHERE hisId =\'{}\'""".format(response.json()['data']["accessToken"], response.json()['data']["refreshToken"], 1,
                                  headers['TimeStampReq'], read_csv()[0])

    sqlite().sqlite_update_time(sql)
    info = response.json()['data']["permissions"]
    # print(response.json()['data'])
    l = []
    for i in info:
        print(i)
        if len(i['id']) == 5:
            # print(i['id'],i['dcrp'])
            l.append(i['dcrp'])
    dict["user_id"] = response.json()['data']["userId"]
    dict["hisId"] = response.json()['data']["hisId"]
    dict["deptId"] = response.json()['data']["deptId"]
    dict["deptName"] = response.json()['data']["deptName"]
    dict['analysisModel'] = response.json()['data']['analysisModel']
    dict["permissions"] = l

    offline_glu.get_analysisModel(response.json()['data']['analysisModel'])


exec_count = 0


def heart_beat():
    print("---------开始模拟离线数据-----------")
    time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    '''
    模拟离线测血糖
    '''
    sql = 'select * from patient limit 1'
    i = sqlite().select_id(sql)[0]
    sql = """INSERT INTO "glucose"
           ("uid", "id", "measureId", "userId", "iptNum", "deptId", "name", "bedNum", "timeType", "timeSlot", "measureType", "value", "deviceNo", "method", "measureTime", "unusual", "nurseId", "nurseName", "valueUnit", "updateTime", "comment", "status", "type", "color", "bedSort")
           VALUES (NULL, NULL, NULL, \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', '午餐后', '午餐后', 1, 5.5, '359A00004C2', 0, \'{}\', 2, \'{}\', \'{}\', 1, NULL, '', 1, 1, 2, '')""".format(
        i[0], i[1], i[6], i[2], str(i[4]), time1, dict["user_id"], read_csv()[0])
    # sqlite().insert(sql)
    '''
    模拟离线质控
    '''
    sql = """select * from paper"""
    paper = sqlite().select_gloucose_islogin(sql)[0]
    paperId = paper[0]
    paperBatchNum = paper[1]
    paperProductionDate = paper[4]
    paperExpiryDate = paper[5]
    sql = """select * from liquid"""
    liquid = sqlite().select_gloucose_islogin(sql)[0]
    liquidId = liquid[0]
    liquidBatchNum = liquid[2]
    liquidProductionDate = liquid[5]
    liquidExpiryDate = liquid[6]
    type = liquid[4]
    if type == 0:
        low = paper[7]
        high = paper[6]
    if type == 1:
        low = paper[9]
        high = paper[8]
    if type == 2:
        low = paper[11]
        high = paper[10]
    sql = """INSERT INTO
        "quality_control"("uid", "id", "value", "sn", "result", "measureTime", "operatorUserName", "operatorUserId",
                          "deptId", "deptName", "paperId", "paperOpenTime", "paperBatchNum", "paperProductionDate",
                          "paperExpiryDate", "liquidId", "liquidBatchNum", "liquidOpenTime", "liquidProductionDate",
                          "liquidExpiryDate", "type", "low", "high", "remote", "status")
        VALUES(NULL, NULL, 6.0, \'{}\', 0, \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', '', \'{}\',
               \'{}\', \'{}\', \'{}\', \'{}\', '', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', 1, 1)""".format(

        headers['Sn'], time1, dict['hisId'], dict['user_id'], dict['deptId'], dict['deptName'], paperId,
        paperBatchNum,
        paperProductionDate, paperExpiryDate, liquidId, liquidBatchNum, liquidProductionDate, liquidExpiryDate,
        type,
        low, high)
    # sqlite().insert(sql)
    '''
    模拟离线室间质评
    '''

    sql = """INSERT INTO
            "external_quality_assessment"("uid", "id", "sn", "measureTime", "batchNum", "sampleNum", "value", "nurseId", "type")
            VALUES(NULL, '', \'{}\', \'{}\', '2', '3', 17.2999992370605, \'{}\', 1)""".format(
        headers['Sn'], time1, dict['user_id'],
    )
    # sqlite().insert(sql)
    '''
    模拟离线对比测试
    '''
    sql = """INSERT INTO
    "compare_test_record"("uid", "id", "result", "unusual", "detectionTime", "paperId", "paperBatchNum",
                          "operatorUserId", "sampleNo", "status", "remote")
    VALUES(NULL, NULL, 15, 1,\'{}\' , \'{}\', \'{}\', \'{}\', '8', 1, 0)""".format(
        time1, paperId, paperBatchNum, dict['user_id']
    )
    sqlite().insert(sql)
    print("---------离线数据模拟完成-----------")
    print(time1)
    DownloadAndUpload(time1)

    print("---------开启一分钟的定时器-----------")
    global exec_count
    exec_count += 1
    if exec_count < 1:
        threading.Timer(60, heart_beat).start()

if __name__ == '__main__':
    # name = input("设备首次入库请输入1，下拉初始离线数据：")
    # if name == '1':
    #     before_login()
    login()
    print(dict["permissions"])
    # before_login()
    print("---------用户开始登陆-----------")
    login()
    print("---------用户登陆完成-----------")

    heart_beat()

