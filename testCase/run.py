# coding=UTF-8
import os
import sys
import requests
import time
from common.read_yaml import load

sys.path.append(r'' + os.path.abspath('../'))
import pytest, yaml
from testCase.log import logger
from common.yaml_util import \
    clear_yaml, write_yaml, read_yaml, clear_menzhen_yaml, read_url_csv, read_csv, \
    write_menzhen_yaml, write_menzhen_blood_yaml, clear_menzhen_blood_yaml, write_zy_yaml, \
    clear_zy_yaml, write_zy_blood_yaml, clear_zy_blood_yaml, write_order_yaml, clear_order_yaml, \
    write_zy_temp_blood_yaml, clear_zy_temp_blood_yaml, read_zy_yaml
from common.Yaml import patient_yaml
# from testCase.get_basic import mz, zy, zy_temp
import testCase.get_basic as A
import json

url = read_url_csv()[0]
headers = {
    "Content-Type": "application/json;charset=UTF-8",
    "Accept": "application/json, text/plain, */*",
    "Project": "vivachekcloud",
    "Platform": "3",
    "Version": "v1.7.0",
    "X-User-Agent": "ios/8.1",
    "Connection": "keep-alive"
}


def login():
    try:
        response = requests.post(url.format('login'), headers=headers, data=json.dumps({"hisId": read_csv()[0],
                                                                                       "password": read_csv()[1]}))

        print(response)
    except AssertionError:
        logger.getlogger().error("请检查请求头、请求地址或者后台服务是否正常")
    if response.status_code == 200:
        headers["Access-Token"] = response.json()['data']['accessToken']
        headers["refresh_token"] = response.json()['data']['refreshToken']
        write_yaml({'headers': headers})

        write_yaml({"userId": response.json()['data']["userId"]})
        try:
            write_yaml({"deptId": response.json()['data']["deptId"]})
        except:
            pass

        write_yaml({"hosId": response.json()['data']["hosId"]})
        info = response.json()['data']["permissions"]
        l = []
        for i in info:
            l.append(i['dcrp'])
        write_yaml({"permissions": l})
    else:
        logger.getlogger().error(response.json())


if __name__ == '__main__':
    clear_yaml()
    login()
    inhos_patient_path='../data/inhos_patient/'
    inhos_patient_list = inhos_patient_path + 'inhos_patient_list.yaml'
    # inhos_patient_list_leave = '../data/inhos_patient/inhos_patient_list_leave.yaml'
    # inhos_patient_info = '../data/inhos_patient/inhos_patient_info.yaml'
    # inhos_patient_healthArchives = '../data/inhos_patient/inhos_patient_info_healthArchives.yaml'
    # inhos_patient_changebed = '../data/inhos_patient/inhos_patient_changebed.yaml'
    # inhos_patient_update = '../data/inhos_patient/inhos_patient_info_update.yaml'
    # inhos_patient_add = '../data/inhos_patient/inhos_patient_info_add.yaml'

    # pytest.main(["--clean-alluredir", '--alluredir', '../result'])

    '''
    此账号如果有门诊权限，获取今日门诊最新患者的个人信息以及
    他的第一条血糖
    '''
    # if "门诊管理" in read_yaml('permissions'):
    #     response = requests.post(url.format('mz/patient/list'), headers=read_yaml('headers'),
    #                              data=mz().get_patient_info()).json()
    #     if response['data']['count'] != 0:
    #         info = requests.post(url.format('mz/patient/info'), headers=read_yaml('headers'),
    #                              data=json.dumps({"userId": response['data']['lists'][0]['userId']})).json()
    #         write_menzhen_yaml(info['data'])
    #         response = requests.post(url.format('mz/glu/list'), headers=read_yaml('headers'),
    #                              data=mz().get_blood_info()).json()
    #         if response['data']['count'] == 0:
    #             response = requests.post(url.format('mz/glu/add'), headers=read_yaml('headers'),
    #                                      data=mz().add_glu()).json()
    #         response1 = requests.post(url.format('mz/glu/list'), headers=read_yaml('headers'),
    #                              data=mz().get_blood_info()).json()
    #     # print(response1['data']['lists'])
    #         write_menzhen_blood_yaml(response1['data']['lists'][0])
    #
    # pytest.main(["-sv", './test_menzhen/test_patient.py'])
    #     # pytest.main(["-sv", './test_menzhen/test_blood.py'])
    #     pytest.main([ "-sv", './test_menzhen/test_patient.py', '--alluredir', '../result'])
    #     pytest.main(["-sv", './test_menzhen/test_blood.py', '--alluredir', '../result'])
    # #     # os.system(
    # #     #     'allure generate ../result -o ../report_allure --clean')
    if "住院管理" in read_yaml('permissions'):
        '''
        住院患者和患者血糖
        '''
        # response = requests.post(url.format('inhos/patient/list'), headers=read_yaml('headers'),
        #                          data=A.zy().get_patient_info()).json()
        # if response['data']['count'] != 0:
        #     info = requests.post(url.format('inhos/patient/info'), headers=read_yaml('headers'),
        #                          data=json.dumps({"userId": response['data']['lists'][0]['userId']})).json()
            # userid = info['data']['userId']
            # deptId = info['data']['deptId']
            # iptNum = info['data']['iptNum']
            # try:
            #     bedNum = info['data']['bedNum']
            # except:
            #     bedNum = ""
            # try:
            #     birthday = info['data']['birthday']
            # except:
            #     birthday = "1973-12-15"
            # try:
            #     gender = info['data']['gender']
            # except:
            #     gender = 1

            # name = info['data']['name']
            # time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # patient_yaml(file=inhos_patient_list, deptId=deptId, iptNum=iptNum, bedNum=bedNum, name=name)
            # patient_yaml(file=inhos_patient_list_leave, deptId=deptId, iptNum=iptNum, bedNum=bedNum, name=name)
            # patient_yaml(file=inhos_patient_info, userid=userid,iptNum=iptNum)
            # patient_yaml(file=inhos_patient_healthArchives, userid=userid)
            # patient_yaml(file=inhos_patient_changebed, userid=userid)
            # patient_yaml(file=inhos_patient_update, userid=userid,birthday=birthday,gender=gender,deptId=deptId,
            #              iptNum=iptNum,)
            # pytest.main(["-sv", './test_zhuyuan/test_patient.py::Testzhuyuan::test_in_patient'])
            # write_zy_yaml(info['data'])

            # response = requests.post(url.format('inhos/glu/list'), headers=read_yaml('headers'),
            #                          data=A.zy().get_blood_info(userid)).json()
            # if response['data']['count'] == 0:
            #     response = requests.post(url.format('inhos/glu/add'), headers=read_yaml('headers'),
            #                              data=A.zy().add_glu(userid)).json()
            # response1 = requests.post(url.format('inhos/glu/list'), headers=read_yaml('headers'),
            #                           data=A.zy().get_blood_info(userid)).json()
            # write_zy_blood_yaml(response1['data']['lists'][0])

            # '''
            # 医嘱
            # '''
            # info = requests.post(url.format('inhos/measure/glu_order/web_monitorList'), headers=read_yaml('headers'),
            #                      data=zy().get_order()).json()
            #
            # if info['data']['count'] == 0:
            #     respon = requests.post(url.format('inhos/measure/glu_order/add'),
            #                   headers=read_yaml('headers'),
            #                   data=zy().add_order()).json()
            # response1 = requests.post(url.format('inhos/measure/glu_order/web_monitorList'), headers=read_yaml('headers'),
            #                           data=zy().get_order()).json()
            #
            # if response1['data']['analysisModel'] == 0:
            #     write_order_yaml({'analysisModel': response1['data']['analysisModel']})
            #     write_order_yaml(response1['data']['lists'][0])
            # if response1['data']['analysisModel'] == 1:
            #     write_order_yaml({'analysisModel': response1['data']['analysisModel']})
            #     for i in response1['data']['lists']:
            #         i['status'] = 1
            #         write_order_yaml(i)
            #         break
            # '''
            # 临时检测
            # '''
            # response = requests.post(url.format('inhos/measure/temp/list'), headers=read_yaml('headers'),
            #                          data=zy_temp().tmep_glu_list()).json()
            # if response['data']['count'] == 0:
            #     response = requests.post(url.format('inhos/measure/temp/add'), headers=read_yaml('headers'),
            #                              data=zy_temp().add_glu()).json()
            #
            # response1 = requests.post(url.format('inhos/measure/temp/list'), headers=read_yaml('headers'),
            #                           data=zy_temp().tmep_glu_list()
            #                           ).json()
            # write_zy_temp_blood_yaml(response1['data']['lists'][0])
        # pytest.main(["-sv", './test_zhuyuan/test_patient.py::Testzhuyuan::test_update_patient_info'])
        # pytest.main(["-sv", './test_zhuyuan/test_patient.py'])
        # pytest.main(["-sv", './test_zhuyuan/test_patient_blood.py'])
        # pytest.main(["-sv", './test_zhuyuan/test_order.py'])
        # pytest.main(["-sv", './test_zhuyuan/test_temp_blood.py'])
        # pytest.main(["-sv", './test_zhuyuan/test_warning.py'])
        # pytest.main(["-sv", './test_zhuyuan/test_patient.py', '--alluredir', '../result'])
        # pytest.main(["-sv", './test_zhuyuan/test_patient_blood.py', '--alluredir', '../result'])
        # pytest.main(["-sv", './test_zhuyuan/test_order.py', '--alluredir', '../result'])
        # pytest.main(["-sv", './test_zhuyuan/test_temp_blood.py', '--alluredir', '../result'])
        # pytest.main(["-sv", './test_zhuyuan/test_warning.py', '--alluredir', '../result'])

        # pytest.main(["-sv", './test_zhuyuan/test_patient_blood.py::Test_zy_blood::test_add_zy_blood'])
        # pytest.main(["-sv", './test_zhuyuan/test_patient_blood.py'])
        # pytest.main(["-sv", './test_zhuyuan/test_warning.py'])

    # if "设备管理" in read_yaml('permissions'):
    #     # pass
    #     # pytest.main(["-sv", './test_devices/test_paper.py'])
    #     # pytest.main(["-sv", './test_devices/test_liquid.py'])
    #     # pytest.main(["-sv", './test_devices/test_dev.py'])
    #     pytest.main(["-s", './test_devices/test_paper.py', '--alluredir', '../result'])
    #     pytest.main(["-s", './test_devices/test_liquid.py', '--alluredir', '../result'])
    #     pytest.main(["-s", './test_devices/test_dev.py', '--alluredir', '../result'])
    #
    # if '质控管理' in read_yaml('permissions'):
    #     # pass
    #     # pytest.main(["-sv", './test_qc/test_qc_record.py'])
    #     pytest.main([ "-s", './test_qc/test_qc_record.py', '--alluredir', '../result'])
    #
    # os.system(
    #     'allure generate ../result -o ../report_allure --clean')
