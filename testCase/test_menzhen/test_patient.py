import os
import sys

sys.path.append(r'' + os.path.abspath('../../'))
import allure
import pytest
import requests
from data.menzhen_patient import mz_patient
from testCase.log import logger
from common.yaml_util import read_yaml, read_mz_yaml, read_bastase_sql, read_url_csv
from common.open_database import MysqlDb
import json,time
url = read_url_csv()[0]

response = requests.post(url.format('mz/patient/list'), headers=read_yaml('headers'),
                             data=mz_patient().in_patient_1()).json()
data = response['data']['lists'][0]['userId']

response = requests.post(url.format('mz/patient/info'), headers=read_yaml('headers'),
                                 data=json.dumps({"userId": data})).json()
data0 = response['data']
print(data0)
data = json.dumps({
                'userId':data0['userId'],
                "name": data0["name"],
                "gender": data0["gender"],
                "birthday": data0["birthday"],
                "primayDocId": data0["primayDocId"],
                "deptId": data0["deptId"],
                "idCard": data0["idCard"],
                "phone": data0["phone"],
                'mzDate': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        })

@allure.feature('门诊患者')
class TestMenzhen(object):

    @allure.title('门诊患者')
    @allure.description('该接口写了3个用例包含今日,历史，所有')
    @pytest.mark.parametrize('info', [mz_patient().in_patient_0(),
                                      mz_patient().in_patient_1(),
                                      mz_patient().in_patient_2()])
    def test_in_patient(self, info):
        logger.getlogger().info('测试的接口:%s', url.format('mz/patient/list'))
        response = requests.post(url.format('mz/patient/list'), headers=read_yaml('headers'),
                                 data=info).json()
        logger.getlogger().info('门诊患者：请求头%s传参%s返回体%s',
                                read_yaml('headers'), info, response)


        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'

        except AssertionError:
            logger.getlogger().error("门诊患者 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.title('门诊患者详情')
    @pytest.mark.parametrize('useid', [mz_patient().patient_info()])
    def test_patient_info(self, useid):
        logger.getlogger().info('测试的接口:%s', url.format('mz/patient/info'))
        response = requests.post(url.format('mz/patient/info'), headers=read_yaml('headers'),
                                 data=useid).json()
        # data0 = MysqlDb().select_db(
        #     "SELECT * FROM {}.`mz_patient` WHERE user_id = \'{}\'".
        #     format(
        #         read_bastase_sql()[4],
        #         read_mz_yaml()['userId']
        #     ))
        logger.getlogger().info('门诊患者详情：请求头%s传参%s返回体%s',
                                read_yaml('headers'), useid, response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'

        except AssertionError:
            logger.getlogger().error("门诊患者详情 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.title('患者所有门诊记录')
    @pytest.mark.parametrize('info', [mz_patient().patient_listRecord()])
    def test_patient_listRecord(self, info):
        logger.getlogger().info('测试的接口:%s', url.format('mz/patient/listRecord'))
        response = requests.post(url.format('mz/patient/listRecord'), headers=read_yaml('headers'),
                                 data=info).json()
        # print(response)
        logger.getlogger().info('患者所有门诊记录：请求头%s传参%s返回体%s',
                                read_yaml('headers'), info, response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'

        except AssertionError:
            logger.getlogger().error("患者所有门诊记录 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.title('历史门诊登记')
    @pytest.mark.parametrize('info', [data])
    def test_patient_register(self, info):
        logger.getlogger().info('测试的接口:%s', url.format('mz/patient/register'))
        response = requests.post(url.format('mz/patient/register'), headers=read_yaml('headers'),
                                 data=info).json()

        logger.getlogger().info('历史门诊登记：请求头%s传参%s返回体%s',
                                read_yaml('headers'), info, response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'

        except AssertionError:
            logger.getlogger().error("历史门诊登记 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
    '''
    # 门诊更新患者信息接口，目前只写了单一用例更换手机号，可通过
    # pytest.mark.parametrize增加用例
    # '''

    @allure.title('更新门诊患者信息')
    @allure.description('门诊更新患者信息接口，目前只写了单一用例更换手机号，可通过pytest.mark.parametrize增加用例')
    @pytest.mark.parametrize('info', [mz_patient().patient_info_update1()])
    def test_patient_update(self, info):
        logger.getlogger().info('测试的接口:%s', url.format('mz/patient/update'))
        response = requests.post(url.format('mz/patient/update'), headers=read_yaml('headers'),
                                 data=info).json()
        logger.getlogger().info('更新门诊患者信息：请求头%s传参%s返回体%s',
                                read_yaml('headers'), info, response)

        data = MysqlDb().select_db(
            "SELECT * FROM {}.`mz_patient` WHERE user_id = \'{}\'".
            format(
                read_bastase_sql()[4],
                read_mz_yaml()['userId']
            ))
        logger.getlogger().info('添加试纸：传参%s返回体%s', info, response)
        try:
            assert data[0]['phone'] == json.loads(info)['phone']
            assert response['code'] == 0
            assert response['msg'] == '请求成功'

        except AssertionError:
            logger.getlogger().error("更新门诊患者信息 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
            assert data[0]['phone'] == json.loads(info)['phone']

    @allure.title('门诊患者登记')
    @allure.description('门诊患者登记接口')
    @pytest.mark.parametrize('info', [mz_patient().patient_info_add0()])
    def test_patient_add(self, info):
        logger.getlogger().info('测试的接口:%s', url.format('mz/patient/add'))
        response = requests.post(url.format('mz/patient/add'), headers=read_yaml('headers'),
                                 data=info).json()
        data = MysqlDb().select_db(
            "SELECT * FROM {}.`mz_patient` WHERE id_card = \'{}\'".
                format(
                read_bastase_sql()[4],
                json.loads(info)['idCard']
            ))
        logger.getlogger().info('门诊患者详情：请求头%s传参%s返回体%s',
                                read_yaml('headers'), info, response)
        try:
            assert data[0]['id_card'] == json.loads(info)['idCard']
            assert response['code'] == 0
            assert response['msg'] == '请求成功'

        except AssertionError:
            logger.getlogger().error("登陆后台 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
            assert data[0]['id_card'] == json.loads(info)['idCard']
