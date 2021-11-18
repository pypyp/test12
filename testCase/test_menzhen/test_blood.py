# coding=UTF-8
import os
import sys

sys.path.append(r'' + os.path.abspath('../../'))
import pytest
import allure
import requests,json
from common.open_database import MysqlDb
from common.yaml_util import read_yaml, read_mz_yaml, read_bastase_sql, read_url_csv ,clear_menzhen_blood_yaml
from testCase.log import logger
from data.menzhen_blood import mz_blood
url = read_url_csv()[0]
@allure.feature("门诊血糖")
class Testblood():
    '''
    考虑数据添加的血糖数据太多，目前只增加一条正确的血糖
    '''
    @allure.title('门诊血糖添加')
    @pytest.mark.parametrize('info', [mz_blood().add_zy_glu0(),
                                      mz_blood().add_zy_glu1(),
                                      mz_blood().add_zy_glu2(),
                                      mz_blood().add_zy_glu3(),
                                      mz_blood().add_zy_glu4(),
                                      mz_blood().add_zy_glu5(),
                                      mz_blood().add_zy_glu6(),
                                      mz_blood().add_zy_glu7(),
                                      mz_blood().add_zy_glu8(),
                                      mz_blood().add_zy_glu9(),
                                      ])
    def test_add_menzhen_blood(self,info):
        logger.getlogger().info('测试的接口:%s',url.format('mz/glu/add'))
        response = requests.post(url.format('mz/glu/add'), headers=read_yaml('headers'),
                                 data=info).json()
        logger.getlogger().info('添加血糖信息：请求头%s传参%s返回体%s',
                                read_yaml('headers'), info, response)
        data = MysqlDb().select_db(
            "select * from {}.`blood_glucose_record` where  comment=\'{}\' and user_id=\'{}\' ORDER BY id DESC limit 1".format(
                read_bastase_sql()[4],
                json.loads(info)['comment'],
                read_mz_yaml()['userId']
            ))

        try:
            assert str(data[0]['measure_time']) == json.loads(info)['measureTime']
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("添加血糖 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
            assert str(data[0]['measure_time']) == json.loads(info)['measureTime']

    @allure.title('门诊患者血糖列表')
    @pytest.mark.parametrize('info', [mz_blood().menzhen_patient_glu()])
    def test_menzhen_glu_list(self,info):
        logger.getlogger().info('测试的接口:%s', url.format('mz/glu/list'))
        response=requests.post(url.format('mz/glu/list'),headers=read_yaml('headers'),data=info).json()
        print(response)
        logger.getlogger().info('门诊患者血糖列表：请求头%s传参%s返回体%s',
                                read_yaml('headers'), info, response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'

        except AssertionError:
            logger.getlogger().error("门诊患者血糖列表 %s", "接口报错", exc_info=1)
            assert response['code'] == 0


    @allure.title('门诊患者血糖修改')

    @pytest.mark.parametrize('info', [mz_blood().menzhen_patient_glu_update1(),
                                          mz_blood().menzhen_patient_glu_update2()])
    def test_menzhen_glu_update(self, info):
        logger.getlogger().info('测试的接口:%s', url.format('mz/glu/update'))
        response = requests.post(url.format('mz/glu/update'), headers=read_yaml('headers'), data=info).json()
        logger.getlogger().info('门诊患者血糖修改：请求头%s传参%s返回体%s',
                                read_yaml('headers'), info, response)

        data = MysqlDb().select_db(
            "select * from {}.`blood_glucose_record` where user_id=\'{}\' and id=\'{}\'".format(
                read_bastase_sql()[4],
                read_mz_yaml()['userId'],
                json.loads(info)['id'], ))
        try:
            assert data[0]['time_type'] == json.loads(info)['timeType']
            assert data[0]['value'] == json.loads(info)['value']
            assert response['code'] == 0
            assert response['msg'] == '请求成功'

        except AssertionError:
            logger.getlogger().error("门诊患者血糖修改 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
            assert data[0]['time_type'] == json.loads(info)['timeType']
            assert data[0]['value'] == json.loads(info)['value']

    @allure.title('门诊患者血糖删除')
    @pytest.mark.parametrize('info', [mz_blood().menzhen_patient_glu_del()])
    def test_menzhen_glu_del(self, info):
        logger.getlogger().info('测试的接口:%s', url.format('mz/glu/delete'))
        response = requests.post(url.format('mz/glu/delete'), headers=read_yaml('headers'), data=info).json()
        logger.getlogger().info('门诊患者血糖删除：请求头%s传参%s返回体%s',
                                read_yaml('headers'), info, response)
        data = MysqlDb().select_db(
            "select * from {}.`blood_glucose_record` where user_id=\'{}\' and id=\'{}\'".format(
                read_bastase_sql()[4],
                read_mz_yaml()['userId'],
                json.loads(info)['id'], ))
        try:
            assert data[0]['status'] == 0
            assert response['code'] == 0
            assert response['msg'] == '请求成功'

        except AssertionError:
            logger.getlogger().error("门诊患者血糖删除 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
            assert data[0]['status'] == 0