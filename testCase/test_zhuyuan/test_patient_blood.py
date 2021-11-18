# coding=UTF-8
import os
import sys

sys.path.append(r'' + os.path.abspath('../../'))
import pytest
import allure
import requests
from common.yaml_util import read_yaml, read_url_csv, read_bastase_sql, read_zy_yaml
from testCase.log import logger
from common.open_database import MysqlDb
from data.zy_blood import zy_blood
import json

url = read_url_csv()[0]


@allure.feature("住院患者血糖")
class Test_zy_blood():
    @allure.title('住院患者血糖列表')
    @allure.description('该接口写了3个用例，本次住院，上次住院，全部住院')
    @pytest.mark.parametrize('info', [zy_blood().zy_patient_glu1(),
                                      zy_blood().zy_patient_glu2(),
                                      zy_blood().zy_patient_glu3()])
    def test_zy_glu_list(self, info):
        logger.getlogger().info('测试的接口:%s', url.format('inhos/glu/list'))
        response = requests.post(url.format('inhos/glu/list'), headers=read_yaml('headers'), data=info).json()
        print(response)
        logger.getlogger().info('住院患者血糖列表：请求头%s传参%s返回体%s',
                                read_yaml('headers'), info, response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'

        except AssertionError:
            logger.getlogger().error("住院患者血糖列表 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.title('住院患者血糖报告')
    @pytest.mark.parametrize('info', [zy_blood().zy_patient_glu_report1(),
                                      zy_blood().zy_patient_glu_report2(),
                                      zy_blood().zy_patient_glu_report3()])
    @allure.description('该接口写了3个用例，本次住院，上次住院，全部住院')
    def test_zy_glu_report(self, info):
        logger.getlogger().info('测试的接口:%s', url.format('inhos/glu/report'))
        response = requests.post(url.format('inhos/glu/report'), headers=read_yaml('headers'), data=info).json()

        logger.getlogger().info('住院患者血糖报告：请求头%s传参%s返回体%s',
                                read_yaml('headers'), info, response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'

        except AssertionError:
            logger.getlogger().error("住院患者血糖报告 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    '''
    web端患者血糖添加
    '''

    @allure.title('住院血糖添加')
    @pytest.mark.parametrize('info', [zy_blood().add_zy_glu0(),
                                      zy_blood().add_zy_glu1(),
                                      zy_blood().add_zy_glu2(),
                                      zy_blood().add_zy_glu3(),
                                      zy_blood().add_zy_glu4(),
                                      zy_blood().add_zy_glu5(),
                                      zy_blood().add_zy_glu6(),
                                      zy_blood().add_zy_glu7(),
                                      zy_blood().add_zy_glu8(),
                                      zy_blood().add_zy_glu9(),

                                      ])
    @allure.description('该接口写了10个用例，正常血糖，33.3，0.6，以及各种状态')
    def test_add_zy_blood(self, info):
        logger.getlogger().info('测试的接口:%s', url.format('inhos/glu/add'))
        response = requests.post(url.format('inhos/glu/add'), headers=read_yaml('headers'),
                                 data=info).json()
        logger.getlogger().info('添加血糖信息：请求头%s传参%s返回体%s',
                                 read_yaml('headers'), info, response)
        data = MysqlDb().select_db(
            "select * from {}.`blood_glucose_record` where  comment=\'{}\' and user_id=\'{}\' ORDER BY id DESC limit 1".format(
                read_bastase_sql()[4],
                json.loads(info)['comment'],
                read_zy_yaml()['userId']
            ))
        print(data[0]['measure_time'],json.loads(info)['measureTime'])
        try:
            assert str(data[0]['measure_time']) == json.loads(info)['measureTime']
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("添加血糖 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
            assert str(data[0]['measure_time']) == json.loads(info)['measureTime']

    #
    @allure.title('住院患者血糖趋势图')
    @pytest.mark.parametrize('info', [zy_blood().patientTrendChart()])
    def test_patientTrendChart(self, info):
        logger.getlogger().info('测试的接口:%s', url.format('inhos/glu/patientTrendChart'))
        response = requests.post(url.format('inhos/glu/patientTrendChart'), headers=read_yaml('headers'),
                                 data=info).json()
        logger.getlogger().info('住院患者血糖趋势图：请求头%s传参%s返回体%s',
                                read_yaml('headers'), info, response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("患者血糖趋势 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.title('住院患者血糖统计图')
    @pytest.mark.parametrize('info', [zy_blood().patientPieChart()])
    def test_patientPieChart(self, info):
        logger.getlogger().info('测试的接口:%s', url.format('inhos/glu/patientPieChart'))
        response = requests.post(url.format('inhos/glu/patientPieChart'), headers=read_yaml('headers'),
                                 data=info).json()
        logger.getlogger().info('门诊患者血糖统计图：请求头%s传参%s返回体%s',
                                read_yaml('headers'), info, response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("患者血糖统计图 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    '''
    血糖修改修改时段和血糖值
    '''

    @allure.title('住院患者血糖修改')
    @allure.description('更新血糖，目前写了两个用例，修改时段，修改血糖值')
    @pytest.mark.parametrize('info', [zy_blood().zy_patient_glu_update1(),
                                      zy_blood().zy_patient_glu_update2()])
    def test_zy_glu_update(self, info):
        logger.getlogger().info('测试的接口:%s', url.format('inhos/glu/update'))
        response = requests.post(url.format('inhos/glu/update'), headers=read_yaml('headers'), data=info).json()
        logger.getlogger().info('住院患者血糖修改：请求头%s传参%s返回体%s',
                                read_yaml('headers'), info, response)
        data = MysqlDb().select_db(
            "select * from {}.`blood_glucose_record` where user_id=\'{}\' and id=\'{}\'".format(
                read_bastase_sql()[4],
                read_zy_yaml()['userId'],
                json.loads(info)['id'], ))
        try:
            assert data[0]['time_type'] == json.loads(info)['timeType']
            assert data[0]['value'] == json.loads(info)['value']
            assert response['code'] == 0
            assert response['msg'] == '请求成功'

        except AssertionError:
            logger.getlogger().error("住院患者血糖修改 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
            assert data[0]['time_type'] == json.loads(info)['timeType']
            assert data[0]['value'] == json.loads(info)['value']

    @allure.title('住院患者血糖删除')
    @pytest.mark.parametrize('info', [zy_blood().zy_patient_glu_del0()])
    def test_zy_glu_del(self, info):
        logger.getlogger().info('测试的接口:%s', url.format('inhos/glu/delete'))
        response = requests.post(url.format('inhos/glu/delete'), headers=read_yaml('headers'), data=info).json()
        logger.getlogger().info('住院患者血糖删除：请求头%s传参%s返回体%s',
                                read_yaml('headers'), info, response)
        data = MysqlDb().select_db(
            "select * from {}.`blood_glucose_record` where user_id=\'{}\' and id=\'{}\'".format(
                read_bastase_sql()[4],
                read_zy_yaml()['userId'],
                json.loads(info)['id'], ))

        try:
            assert data[0]['status'] == 0
            assert response['code'] == 0
            assert response['msg'] == '请求成功'

        except AssertionError:
            logger.getlogger().error("住院患者血糖删除 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
            assert data[0]['status'] == 0