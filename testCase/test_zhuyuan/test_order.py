# coding=UTF-8
import os
import sys

sys.path.append(r'' + os.path.abspath('../../'))
import allure
import pytest
import requests
from testCase.log import logger
from common.yaml_util import read_yaml, read_bastase_sql, read_url_csv
from common.open_database import MysqlDb
import json, yaml
from data.read_fun import read_yaml_info
from common.read_yaml import load

url = read_url_csv()[0]


@allure.feature('医嘱')
class Test_order(object):

    @allure.title('根据任务是不是解析是解析则添加血糖')
    @pytest.mark.parametrize('info',
                             yaml.safe_load(read_yaml_info(
                                 load('../data/path/path.yaml')['glu_order_addMeasure'])))
    def test_glu_order_addmeasure(self,info):

        if info["analysisModel"] == 0:
            logger.getlogger().info('任务不解析')
        else:
            response = requests.post(url.format('inhos/measure/glu_order/addMeasure'),
                                     headers=read_yaml('headers'),
                                     data=json.dumps(info['parame'])).json()
            logger.getlogger().info('inhos/measure/glu_order/addMeasure：请求头%s'
                                    '传参%s'
                                    '返回体%s',
                                    read_yaml('headers'),
                                    info['parame'],
                                    response)

            data = MysqlDb().select_db(
          "select * from {}.`blood_glucose_record` where measure_id=\'{}\'".format(read_bastase_sql()[4],
                                                                                   info['parame']['id']))

            try:
                assert data[0]['value'] == info['parame']['value']
                assert response['code'] == info['result']['code']
                assert response['msg'] == info['result']['msg']
            except AssertionError:
                logger.getlogger().error("inhos/measure/glu_order/addMeasure %s", "接口报错", exc_info=1)
                assert data[0]['value'] == info['parame']['value']
                assert response['code'] == info['result']['code']
            logger.getlogger().info('---->接口:%s结束一次用例测试', url.format('inhos/measure/glu_order/addMeasure'))

    @allure.title('患者任务列表')
    @pytest.mark.parametrize('info',
                             yaml.safe_load(read_yaml_info(
                                 load('../data/path/path.yaml')['inhos_measure_glu_order_webOrderList'])))
    def test_glu_order_webOrderList(self, info):
        logger.getlogger().info('---->接口:%s开始测试', url.format('inhos/measure/glu_order/web_monitorList'))
        response = requests.post(url.format('inhos/measure/glu_order/web_monitorList'),
                                 headers=read_yaml('headers'),
                                 data=json.dumps(info['parame'])).json()
        logger.getlogger().info('inhos/measure/glu_order/web_monitorList：请求头%s'
                                '传参%s'
                                '返回体%s',
                                read_yaml('headers'),
                                info['parame'],
                                response)
        try:
            assert response['code'] == info['result']['code']
            assert response['msg'] == info['result']['msg']
        except AssertionError:
            logger.getlogger().error("inhos/measure/glu_order/web_monitorList %s", "接口报错", exc_info=1)
            assert response['code'] == info['result']['code']
        logger.getlogger().info('---->接口:%s结束一次用例测试', url.format('inhos/measure/glu_order/web_monitorList'))

    @allure.title('患者任务列表')
    @pytest.mark.parametrize('info',
                             yaml.safe_load(read_yaml_info(
                                 load('../data/path/path.yaml')['inhos_measure_glu_order_getPatientOrderList'])))
    def test_glu_order_getPatientOrderList(self, info):

        logger.getlogger().info('---->接口:%s开始测试', url.format('inhos/measure/glu_order/getPatientOrderList'))
        response = requests.post(url.format('inhos/measure/glu_order/getPatientOrderList'), headers=read_yaml('headers'),
                                 data=json.dumps(info['parame'])).json()
        logger.getlogger().info('inhos/measure/glu_order/getPatientOrderList：请求头%s'
                                '传参%s'
                                '返回体%s',
                                read_yaml('headers'),
                                info['parame'],
                                response)
        data = MysqlDb().select_db("select count(*) from {}.`medical_order`where user_id=\'{}\'".format(read_bastase_sql()[4],
                                                                                                    info['parame']['userId']))

        try:
            assert response['data']['headInfo']['num1'] == data[0]['count(*)']
            assert response['code'] == info['result']['code']
            assert response['msg'] == info['result']['msg']
        except AssertionError:
            logger.getlogger().error("inhos/measure/glu_order/getPatientOrderList %s", "接口报错", exc_info=1)
            assert response['code'] == info['result']['code']
            assert response['data']['headInfo']['num1'] == data[0]['count(*)']
        logger.getlogger().info('---->接口:%s结束一次用例测试', url.format('inhos/measure/glu_order/getPatientOrderList'))

    @allure.title('患者详情')
    @pytest.mark.parametrize('info',
                             yaml.safe_load(read_yaml_info(
                                 load('../data/path/path.yaml')['inhos_measure_glu_order_info'])))
    def test_glu_order_info(self, info):

        logger.getlogger().info('---->接口:%s开始测试', url.format('inhos/measure/glu_order/info'))
        response = requests.post(url.format('inhos/measure/glu_order/info'),
                                 headers=read_yaml('headers'),
                                 data=json.dumps(info['parame'])).json()
        logger.getlogger().info('inhos/measure/glu_order/info：请求头%s'
                                '传参%s'
                                '返回体%s',
                                read_yaml('headers'),
                                info['parame'],
                                response)
        try:
            assert response['code'] == info['result']['code']
            assert response['msg'] == info['result']['msg']
        except AssertionError:
            logger.getlogger().error("inhos/measure/glu_order/info %s", "接口报错", exc_info=1)
            assert response['code'] == info['result']['code']
        logger.getlogger().info('---->接口:%s结束一次用例测试', url.format('inhos/measure/glu_order/info'))

    @allure.title('编辑任务')
    @pytest.mark.parametrize('info',
                             yaml.safe_load(read_yaml_info(
                                 load('../data/path/path.yaml')['inhos_measure_glu_order_update'])))
    def test_glu_order_update(self, info):
        logger.getlogger().info('---->接口:%s开始测试', url.format('inhos/measure/glu_order/update'))
        response = requests.post(url.format('inhos/measure/glu_order/update'),
                                 headers=read_yaml('headers'),
                                 data=json.dumps(info['parame'])).json()
        logger.getlogger().info('inhos/measure/glu_order/update：请求头%s'
                                '传参%s'
                                '返回体%s',
                                read_yaml('headers'),
                                info['parame'],
                                response)
        data = MysqlDb().select_db(
                "select * from {}.`medical_order`order by id desc ".format(read_bastase_sql()[4],
                                                                                ))

        try:
            assert data[0]['time_type'] == info['parame']['timeType']
            assert data[0]['entrust'] == info['parame']['entrust']
            assert response['code'] == info['result']['code']
            assert response['msg'] == info['result']['msg']
        except AssertionError:
            logger.getlogger().error("inhos/measure/glu_order/update %s", "接口报错", exc_info=1)
            assert response['code'] == info['result']['code']
            assert data[0]['time_type'] == info['parame']['timeType']
            assert data[0]['entrust'] == info['parame']['entrust']
        logger.getlogger().info('---->接口:%s结束一次用例测试', url.format('inhos/measure/glu_order/update'))

    @allure.title('停止任务')
    @pytest.mark.parametrize('info',
                             yaml.safe_load(read_yaml_info(
                                 load('../data/path/path.yaml')['inhos_measure_glu_order_stop'])))
    def test_glu_order_stop(self, info):
        logger.getlogger().info('---->接口:%s开始测试', url.format('inhos/measure/glu_order/stop'))
        response = requests.post(url.format('inhos/measure/glu_order/getPatientOrderList'),
                                 headers=read_yaml('headers'),
                                 data=json.dumps(info['userid'])).json()
        logger.getlogger().info({'list':response['data']['list']})
        for i in response['data']['list']:
            if i['status']==1:
                info['parame']['id'] = i['id']
            response = requests.post(url.format('inhos/measure/glu_order/stop'),
                                     headers=read_yaml('headers'),
                                     data=json.dumps(info['parame'])).json()
            logger.getlogger().info('inhos/measure/glu_order/stop：请求头%s'
                                    '传参%s'
                                    '返回体%s',
                                    read_yaml('headers'),
                                    info['parame'],
                                    response)
            data = MysqlDb().select_db(
                    "select * from {}.`medical_order`order by id desc ".format(read_bastase_sql()[4],
                                                                                    ))

            try:
                assert data[0]['status'] == 3
                assert response['code'] == info['result']['code']
                assert response['msg'] == info['result']['msg']
            except AssertionError:
                logger.getlogger().error("inhos/measure/glu_order/stop %s", "接口报错", exc_info=1)
                assert response['code'] == info['result']['code']
                assert data[0]['status'] == 3
            logger.getlogger().info('---->接口:%s结束一次用例测试', url.format('iinhos/measure/glu_order/stop'))

            break
