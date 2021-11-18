import os
import sys

sys.path.append(r'' + os.path.abspath('../../'))
import allure
import pytest
import requests
from data.zy_web_order import zy_web_order
from testCase.log import logger
from common.yaml_util import read_yaml, read_zy_yaml, read_bastase_sql, read_url_csv,read_order_yaml
from common.open_database import MysqlDb
import json,time
url = read_url_csv()[0]
@allure.feature('医嘱')
class Test_order(object):

    @allure.title('根据任务是不是解析是解析则添加血糖')
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize('info', [zy_web_order().add_order_glu()])
    def test_glu_order_addmeasure(self,info):

        if read_order_yaml()["analysisModel"] == 0:
            logger.getlogger().info('任务不解析')
        else:
            response = requests.post(url.format('inhos/measure/glu_order/addMeasure'),
                                     headers=read_yaml('headers'),
                                     data=info).json()
            logger.getlogger().info('患者任务列表信息：传参%s返回体%s', info, response)
            data = MysqlDb().select_db(
          "select * from {}.`blood_glucose_record` where measure_id=\'{}\'".format(read_bastase_sql()[4],
                                                                                     read_order_yaml()[
                                                                                         'id']))

            try:
                assert data[0]['value'] == json.loads(info)['value']
                assert data[0]['measure_time'] == json.loads(info)['measureTime']
                assert response['code'] == 0
                assert response['msg'] == '请求成功'
            except AssertionError:
                logger.getlogger().error("患者任务列表 %s", "接口报错", exc_info=1)
                assert response['code'] == 0
                assert data[0]['value'] == json.loads(info)['value']
                assert str(data[0]['measure_time']) == str(json.loads(info)['measureTime'])

    @allure.title('患者任务列表')
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize('info', [zy_web_order().glu_order_getPatientOrderList()])
    def test_glu_order_getPatientOrderList(self,info):
        logger.getlogger().info('测试的接口:%s', url.format('inhos/measure/glu_order/getPatientOrderList'))
        response = requests.post(url.format('inhos/measure/glu_order/getPatientOrderList'), headers=read_yaml('headers'),
                                 data=info).json()
        data = MysqlDb().select_db("select count(*) from {}.`medical_order`where user_id=\'{}\'".format(read_bastase_sql()[4],
                                                                                                read_order_yaml()[
                                                                                                    'userId']))
        logger.getlogger().info('患者任务列表信息：传参%s返回体%s', info, response)
        try:
            assert response['data']['headInfo']['num1'] == data[0]['count(*)']
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("患者任务列表 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
            assert response['data']['headInfo']['num1'] == data[0]['count(*)']

    @allure.title('任务详情')
    @pytest.mark.run(order=3)
    @pytest.mark.parametrize('info', [zy_web_order().glu_order_info()])
    def test_glu_order_info(self,info):
        logger.getlogger().info('测试的接口:%s', url.format('inhos/measure/glu_order/info'))
        response = requests.post(url.format('inhos/measure/glu_order/info'), headers=read_yaml('headers'),
                                 data=info).json()

        data = MysqlDb().select_db("select * from {}.`medical_order_detail`where id=\'{}\' ".format(read_bastase_sql()[4],
                                                                                                read_order_yaml()[
                                                                                                    'id']))
        logger.getlogger().info('患者任务列表信息：传参%s返回体%s', info, response)
        try:
            # assert data[0]['time_type'] == read_order_yaml()['timeType']
            assert str(data[0]['start_time']) == read_order_yaml()['startTime']
            # assert str(data[0]['end_time'])== read_order_yaml()['endTime']
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("患者任务列表 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
            # assert data[0]['time_type'] == read_order_yaml()['timeType']
            assert str(data[0]['start_time']) == read_order_yaml()['startTime']
            # assert str(data[0]['end_time']) == read_order_yaml()['endTime']

    @allure.title('编辑任务')
    @pytest.mark.run(order=4)
    @pytest.mark.parametrize('info', [zy_web_order().update_glu_order()])
    def test_glu_order_update(self, info):
        logger.getlogger().info('测试的接口:%s', url.format('inhos/measure/glu_order/update'))

        response = requests.post(url.format('inhos/measure/glu_order/update'), headers=read_yaml('headers'),
                                 data=info).json()

        data = MysqlDb().select_db(
            "select * from {}.`medical_order`order by id desc ".format(read_bastase_sql()[4],
                                                                            ))
        logger.getlogger().info('患者任务列表信息：传参%s返回体%s', info, response)
        try:
            assert data[0]['time_type'] == json.loads(info)['timeType']
            assert data[0]['entrust'] == json.loads(info)['entrust']
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("患者任务列表 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
            assert data[0]['time_type'] == json.loads(info)['timeType']
            assert data[0]['entrust'] == json.loads(info)['entrust']

    @allure.title('停止任务')
    @pytest.mark.run(order=5)
    def test_glu_order_stop(self):
        logger.getlogger().info('测试的接口:%s', url.format('inhos/measure/glu_order/stop'))
        data = MysqlDb().select_db(
            "select * from {}.`medical_order`order by id desc ".format(read_bastase_sql()[4],
                                                                       ))
        data1 = json.dumps({
            "id":data[0]['id'],
        })
        response = requests.post(url.format('inhos/measure/glu_order/stop'), headers=read_yaml('headers'),
                                 data=data1).json()
        data2 = MysqlDb().select_db(
            "select * from {}.`medical_order`where id=\'{}\' ".format(read_bastase_sql()[4],
                                                                           json.loads(data1)['id']
                                                                       ))
        logger.getlogger().info('停止任务：传参%s返回体%s', data1, response)
        try:
            assert data2[0]['status'] == 3

            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("停止任务 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
            assert data2[0]['status'] == 3


