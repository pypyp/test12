# coding=UTF-8
import os
import sys

sys.path.append(r'' + os.path.abspath('../../'))
import pytest
import allure
import requests
from data.read_fun import read_yaml_info
from common.yaml_util import read_yaml, read_url_csv, read_bastase_sql
from testCase.log import logger
from common.open_database import MysqlDb
from common.read_yaml import load
import json,yaml

url = read_url_csv()[0]


@allure.feature("住院患者血糖")
class Test_zy_blood():
    @allure.title('住院患者血糖列表')
    @allure.description('该接口写了2个用例,全部血糖和按时间查询')
    @pytest.mark.parametrize('info', yaml.safe_load(read_yaml_info(load('../data/path/path.yaml')['inhos_glu_list'])))
    def test_zy_glu_list(self, info):
        logger.getlogger().info('---->接口:%s开始测试', url.format('inhos/glu/list'))
        response = requests.post(url.format('inhos/glu/list'), headers=read_yaml('headers'), data=json.dumps(info['parame'])).json()
        logger.getlogger().info('inhos/glu/list：请求头%s'
                                '传参%s'
                                '返回体%s',
                                read_yaml('headers'),
                                info['parame'],
                                response)
        try:
            assert response['code'] == info['result']['code']
            assert response['msg'] == info['result']['msg']

        except AssertionError:
            logger.getlogger().error("inhos/glu/list %s", "接口报错", exc_info=1)
            assert response['code'] == info['result']['code']
        logger.getlogger().info('---->接口:%s结束一次用例测试', url.format('inhos/glu/list'))

    @allure.title('住院患者血糖报告')
    @allure.description('该接口写了2个用例,全部血糖和按时间查询')
    @pytest.mark.parametrize('info', yaml.safe_load(read_yaml_info(load('../data/path/path.yaml')['inhos_glus_report'])))
    def test_zy_glu_report(self, info):
        logger.getlogger().info('---->接口:%s开始测试', url.format('inhos/glu/report'))
        response = requests.post(url.format('inhos/glu/report'), headers=read_yaml('headers'), data=json.dumps(info['parame'])).json()

        logger.getlogger().info('inhos/glu/list：请求头%s'
                                '传参%s'
                                '返回体%s',
                                read_yaml('headers'),
                                info['parame'],
                                response)
        try:
            assert response['code'] == info['result']['code']
            assert response['msg'] == info['result']['msg']

        except AssertionError:
            logger.getlogger().error("inhos/glu/report %s", "接口报错", exc_info=1)
            assert response['code'] == info['result']['code']
        logger.getlogger().info('---->接口:%s结束一次用例测试', url.format('inhos/glu/report'))

    '''
    web端患者血糖添加
    '''

    @allure.title('住院血糖添加')
    @pytest.mark.parametrize('info',yaml.safe_load(read_yaml_info(load('../data/path/path.yaml')['inhos_glu_add'])))
    @allure.description('该接口写了10个用例，正常血糖，25.5，0.6，以及各种状态')
    def test_add_zy_blood(self, info):
        logger.getlogger().info('---->接口:%s开始测试', url.format('inhos/glu/add'))
        response = requests.post(url.format('inhos/glu/add'), headers=read_yaml('headers'),
                                 data=json.dumps(info['parame'])).json()
        logger.getlogger().info('inhos/glu/list：请求头%s'
                                '传参%s'
                                '返回体%s',
                                read_yaml('headers'),
                                info['parame'],
                                response)

        data = MysqlDb().select_db(
            "select * from {}.`blood_glucose_record` where  user_id=\'{}\' ORDER BY id DESC limit 1".format(
                read_bastase_sql()[4],
                info['parame']['userId']
            ))
        try:
            info['parame']['comment']
        except:
            info['parame']['comment']=None
        print(data[0]['comment'] ,info['parame']['comment'])
        try:
            assert str(data[0]['measure_time']) == info['parame']['measureTime']
            assert data[0]['comment'] == info['parame']['comment']
            assert response['code'] == info['result']['code']
            assert response['msg'] == info['result']['msg']
        except AssertionError:
            logger.getlogger().error("inhos/glu/add %s", "接口报错", exc_info=1)
            assert response['code'] == info['result']['code']
            assert str(data[0]['measure_time']) == info['parame']['measureTime']
            assert data[0]['comment'] == info['parame']['comment']
        logger.getlogger().info('---->接口:%s结束一次用例测试', url.format('inhos/glu/add'))
    # #
    @allure.title('住院患者血糖趋势图')
    @pytest.mark.parametrize('info', yaml.safe_load(read_yaml_info(load('../data/path/path.yaml')['inhos_glu_patientTrendChart'])))
    def test_patientTrendChart(self, info):
        logger.getlogger().info('---->接口:%s开始测试', url.format('inhos/glu/patientTrendChart'))
        response = requests.post(url.format('inhos/glu/patientTrendChart'), headers=read_yaml('headers'),
                                 data=json.dumps(info['parame'])).json()
        logger.getlogger().info('inhos/glu/patientTrendChart：请求头%s'
                                '传参%s'
                                '返回体%s',
                                read_yaml('headers'),
                                info['parame'],
                                response)
        try:
            assert response['code'] == info['result']['code']
            assert response['msg'] == info['result']['msg']

        except AssertionError:
            logger.getlogger().error("inhos/glu/patientTrendChart %s", "接口报错", exc_info=1)
            assert response['code'] == info['result']['code']
        logger.getlogger().info('---->接口:%s结束一次用例测试', url.format('inhos/glu/patientTrendChart'))

    @allure.title('住院患者血糖统计图')
    @pytest.mark.parametrize('info', yaml.safe_load(read_yaml_info(load('../data/path/path.yaml')['inhos_glu_patientPieChart'])))
    def test_patientPieChart(self, info):
        logger.getlogger().info('---->接口:%s开始测试', url.format('inhos/glu/patientPieChart'))
        response = requests.post(url.format('inhos/glu/patientPieChart'), headers=read_yaml('headers'),
                                 data=json.dumps(info['parame'])).json()
        logger.getlogger().info('inhos/glu/patientPieChart：请求头%s'
                                '传参%s'
                                '返回体%s',
                                read_yaml('headers'),
                                info['parame'],
                                response)
        try:
            assert response['code'] == info['result']['code']
            assert response['msg'] == info['result']['msg']

        except AssertionError:
            logger.getlogger().error("inhos/glu/patientPieChart %s", "接口报错", exc_info=1)
            assert response['code'] == info['result']['code']
        logger.getlogger().info('---->接口:%s结束一次用例测试', url.format('inhos/glu/patientPieChart'))

    '''
    血糖修改修改时段和血糖值
    '''

    @allure.title('住院患者血糖修改')
    @allure.description('更新血糖，目前写了两个用例，修改时段，修改血糖值')
    @pytest.mark.parametrize('info', yaml.safe_load(read_yaml_info(load('../data/path/path.yaml')['inhos_glu_update'])))
    def test_zy_glu_update(self, info):
        logger.getlogger().info('---->接口:%s开始测试', url.format('inhos/glu/update'))
        response = requests.post(url.format('inhos/glu/update'), headers=read_yaml('headers'), data=json.dumps(info['parame'])).json()
        logger.getlogger().info('inhos/glu/update：请求头%s'
                                '传参%s'
                                '返回体%s',
                                read_yaml('headers'),
                                info['parame'],
                                response)
        data = MysqlDb().select_db(
            "select * from {}.`blood_glucose_record` where id=\'{}\'".format(
                read_bastase_sql()[4],
                info['parame']['id']))
        try:
            assert data[0]['time_type'] ==  info['parame']['timeType']
            assert data[0]['value'] ==  info['parame']['value']
            assert data[0]['comment'] == info['parame']['comment']
            assert response['code'] == info['result']['code']
            assert response['msg'] == info['result']['msg']

        except AssertionError:
            logger.getlogger().error("inhos/glu/update %s", "接口报错", exc_info=1)
            assert response['code'] == info['result']['code']
            assert data[0]['time_type'] == json.loads(info)['timeType']
            assert data[0]['value'] == json.loads(info)['value']
            assert data[0]['comment'] == info['parame']['comment']
        logger.getlogger().info('---->接口:%s结束一次用例测试', url.format('inhos/glu/patientPieChart'))

    @allure.title('住院患者血糖删除')
    @pytest.mark.parametrize('info', yaml.safe_load(read_yaml_info(load('../data/path/path.yaml')['inhos_glu_del'])))
    def test_zy_glu_del(self, info):
        logger.getlogger().info('---->接口:%s开始测试', url.format('inhos/glu/delete'))
        response = requests.post(url.format('inhos/glu/delete'), headers=read_yaml('headers'), data=json.dumps(info['parame'])).json()
        logger.getlogger().info('inhos/glu/update：请求头%s'
                                '传参%s'
                                '返回体%s',
                                read_yaml('headers'),
                                info['parame'],
                                response)
        data = MysqlDb().select_db(
            "select * from {}.`blood_glucose_record` where id=\'{}\'".format(
                read_bastase_sql()[4],
                info['parame']['id']) )

        try:
            assert data[0]['status'] == 0
            assert response['code'] == info['result']['code']
            assert response['msg'] == info['result']['msg']

        except AssertionError:
            logger.getlogger().error("inhos/glu/update %s", "接口报错", exc_info=1)
            assert response['code'] == info['result']['code']
            assert data[0]['status'] == 0
        logger.getlogger().info('---->接口:%s结束一次用例测试', url.format('inhos/glu/update'))
