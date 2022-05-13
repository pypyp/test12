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
import datetime,time
from data.read_fun import Load_Basic
url = read_url_csv()[0]


@allure.feature("质控")
class Test_qc_record(object):
    @allure.title('查询质控')
    @pytest.mark.parametrize('info',
                             yaml.safe_load(read_yaml_info(load('../data/path/path.yaml')['qc_record_list'])))
    def test_qc_list(self, info):
        logger.getlogger().info('---->接口:%s开始测试', url.format('qc/record/list'))
        response = requests.post(url.format('qc/record/list'), headers=read_yaml('headers'),
                                 data=json.dumps(info['parame'])).json()
        logger.getlogger().info('qc/record/list：请求头%s'
                                '传参%s'
                                '返回体%s',
                                read_yaml('headers'),
                                info['parame'],
                                response)
        try:
            assert response['code'] == info['result']['code']
            assert response['msg'] == info['result']['msg']

        except AssertionError:
            logger.getlogger().error("qc/record/list %s", "接口报错", exc_info=1)
            assert response['code'] == info['result']['code']
        logger.getlogger().info('---->接口:%s结束一次用例测试', url.format('qc/record/list'))

    @allure.title('编辑质控')
    @pytest.mark.parametrize('info',
                             yaml.safe_load(read_yaml_info(load('../data/path/path.yaml')['qc_record_update'])))
    def test_qc_update(self, info):
        info1 = Load_Basic.read_qc_info()
        logger.getlogger().info('---->接口:%s开始测试', url.format('qc/record/update'))
        if info['parame']['value'] > info1['high'] or info['parame']['value'] < info1['low']:
            info['parame']['result'] = 0
        else:
            info['parame']['result'] = 1

        response = requests.post(url.format('qc/record/update'), headers=read_yaml('headers'),
                                 data=json.dumps(info['parame'])).json()
        logger.getlogger().info('qc/record/update：请求头%s'
                                '传参%s'
                                '返回体%s',
                                read_yaml('headers'),
                                info['parame'],
                                response)
        data = MysqlDb().select_db(
            "select * from {}.`qc_record` where id =\'{}\'".format(read_bastase_sql()[4], info['parame']['id']))

        data[0]['measure_time'] = data[0]['measure_time'].strftime('%Y-%m-%d %H:%M:%S')
        try:
            assert data[0]['value'] == info['parame']['value']
            assert data[0]['result'] == info['parame']['result']
            assert data[0]['measure_time'] == info['parame']['measureTime']
            assert response['code'] == info['result']['code']
            assert response['msg'] == info['result']['msg']

        except AssertionError:
            logger.getlogger().error("qc/record/update %s", "接口报错", exc_info=1)
            assert response['code'] == info['result']['code']
            assert data[0]['value'] == info['parame']['value']
            assert data[0]['result'] == info['parame']['result']
            assert data[0]['measure_time'] == info['parame']['measureTime']
        logger.getlogger().info('---->接口:%s结束一次用例测试', url.format('qc/record/update'))

    @allure.title('删除质控')
    @pytest.mark.parametrize('info',
                             yaml.safe_load(read_yaml_info(load('../data/path/path.yaml')['qc_record_delete'])))
    def test_qc_delete(self, info):

        logger.getlogger().info('---->接口:%s开始测试', url.format('qc/record/delete'))

        response = requests.post(url.format('qc/record/delete'), headers=read_yaml('headers'),
                                 data=json.dumps(info['parame'])).json()
        logger.getlogger().info('qc/record/delete：请求头%s'
                                '传参%s'
                                '返回体%s',
                                read_yaml('headers'),
                                info['parame'],
                                response)
        data = MysqlDb().select_db(
            "select * from {}.`qc_record` where id =\'{}\'".format(read_bastase_sql()[4], info['parame']['id']))

        try:
            assert data[0]['status'] == 0

            assert response['code'] == info['result']['code']
            assert response['msg'] == info['result']['msg']

        except AssertionError:
            logger.getlogger().error("qc/record/delete %s", "接口报错", exc_info=1)
            assert data[0]['status'] == 0
            assert response['code'] == info['result']['code']

        logger.getlogger().info('---->接口:%s结束一次用例测试', url.format('qc/record/delete'))

    @allure.title('添加质控')
    @pytest.mark.parametrize('info',
                             yaml.safe_load(read_yaml_info(load('../data/path/path.yaml')['qc_record_add'])))
    def test_qc_add(self, info):

        logger.getlogger().info('---->接口:%s开始测试', url.format('qc/record/add'))

        response = requests.post(url.format('qc/record/add'), headers=read_yaml('headers'),
                                 data=json.dumps(info['parame'])).json()
        logger.getlogger().info('qc/record/delete：请求头%s'
                                '传参%s'
                                '返回体%s',
                                read_yaml('headers'),
                                info['parame'],
                                response)
        data = MysqlDb().select_db(
                    "select * from {}.`qc_record` order by id desc".format(read_bastase_sql()[4]))
        try:
            assert data[0]['value'] == info['parame']['value']

            assert response['code'] == info['result']['code']
            assert response['msg'] == info['result']['msg']

        except AssertionError:
            logger.getlogger().error("qc/record/add %s", "接口报错", exc_info=1)
            assert data[0]['value'] == info['parame']['value']
            assert response['code'] == info['result']['code']

        logger.getlogger().info('---->接口:%s结束一次用例测试', url.format('qc/record/add'))

    @allure.title('质控分析')
    @pytest.mark.parametrize('info',
                             yaml.safe_load(read_yaml_info(load('../data/path/path.yaml')['qc_record_analysis'])))
    def test_qc_analysis(self, info):
        now = datetime.date.today()
        info['parame']['measureTimeEnd']=datetime.datetime(now.year, now.month, 1).strftime('%Y-%m-%d 00:00:00')
        info['parame']['measureTimeStart'] = time.strftime("%Y-%m-%d 23:59:59", time.localtime())
        logger.getlogger().info('---->接口:%s开始测试', url.format('qc/record/analysis'))
        #
        response = requests.post(url.format('qc/record/analysis'), headers=read_yaml('headers'),
                                 data=json.dumps(info['parame'])).json()
        logger.getlogger().info('qc/record/analysis：请求头%s'
                                '传参%s'
                                '返回体%s',
                                read_yaml('headers'),
                                info['parame'],
                                response)
        try:
            assert response['code'] == info['result']['code']
            assert response['msg'] == info['result']['msg']

        except AssertionError:
            logger.getlogger().error("qc/record/analysis %s", "接口报错", exc_info=1)
            assert response['code'] == info['result']['code']

        logger.getlogger().info('---->接口:%s结束一次用例测试', url.format('qc/record/analysis'))

    @allure.title('质控统计')
    @pytest.mark.parametrize('info',
                             yaml.safe_load(read_yaml_info(load('../data/path/path.yaml')['qc_record_statistics'])))
    def test_qc_statistics(self, info):
        logger.getlogger().info('---->接口:%s开始测试', url.format('qc/record/statistics'))
        #
        response = requests.post(url.format('qc/record/statistics'), headers=read_yaml('headers'),
                                 data=json.dumps(info['parame'])).json()
        logger.getlogger().info('qc/record/statistics：请求头%s'
                                '传参%s'
                                '返回体%s',
                                read_yaml('headers'),
                                info['parame'],
                                response)
        try:
            assert response['code'] == info['result']['code']
            assert response['msg'] == info['result']['msg']

        except AssertionError:
            logger.getlogger().error("qc/record/statistics %s", "接口报错", exc_info=1)
            assert response['code'] == info['result']['code']

        logger.getlogger().info('---->接口:%s结束一次用例测试', url.format('qc/record/statistics'))

