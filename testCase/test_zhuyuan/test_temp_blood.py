# coding=UTF-8
import os
import sys

sys.path.append(r'' + os.path.abspath('../../'))
import pytest
import allure
import requests
from common.yaml_util import read_yaml, read_url_csv, read_bastase_sql, read_zy_yaml
from data.read_fun import read_yaml_info
from testCase.log import logger
from common.read_yaml import load
import json,yaml
from common.open_database import MysqlDb

url = read_url_csv()[0]


@allure.feature("临时检测血糖")
class Test_temp_blood():
    '''
    2条用例,一条没有关联患者，一条关联患者
    '''



    @allure.title('临时检测血糖添加')
    @allure.description('该接口写了2个用例添加临时检测，添加时绑定患者')
    @pytest.mark.parametrize('info', yaml.safe_load(read_yaml_info(load('../data/path/path.yaml')['inhos_measure_temp_add'])))
    def test_add_temp_blood(self, info):
        logger.getlogger().info('---->接口:%s开始测试', url.format('inhos/measure/temp/add'))
        response = requests.post(url.format('inhos/measure/temp/add'), headers=read_yaml('headers'),
                                 data=json.dumps(info['parame'])).json()
        logger.getlogger().info('inhos/measure/temp/list：请求头%s'
                                '传参%s'
                                '返回体%s',
                                read_yaml('headers'),
                                info['parame'],
                                response)
        data = MysqlDb().select_db(
            "select * from {}.`blood_glucose_record` order by id desc".format(
                read_bastase_sql()[4]
            ))
        data[0]['measure_time'] = data[0]['measure_time'].strftime('%Y-%m-%d %H:%M:%S')
        try:
            assert data[0]['value'] == info['parame']['value']
            assert data[0]['measure_time'] == info['parame']['measureTime']
            assert response['code'] == info['result']['code']
            assert response['msg'] == info['result']['msg']

        except AssertionError:
            logger.getlogger().error("inhos/measure/temp/add %s", "接口报错", exc_info=1)
            assert response['code'] == info['result']['code']
            assert data[0]['value'] == info['parame']['value']
            assert data[0]['measure_time'] == info['parame']['measureTime']
        logger.getlogger().info('---->接口:%s结束一次用例测试', url.format('inhos/measure/temp/add'))

    @allure.title('临时检测血糖列表')
    @pytest.mark.parametrize('info',yaml.safe_load(read_yaml_info(load('../data/path/path.yaml')['inhos_measure_temp_list'])))
    def test_temp_glu_list(self, info):
        print(info)
        logger.getlogger().info('---->接口:%s开始测试', url.format('inhos/measure/temp/list'))
        response = requests.post(url.format('inhos/measure/temp/list'), headers=read_yaml('headers'),
                                 data=json.dumps(info['parame'])).json()

        logger.getlogger().info('inhos/measure/temp/list：请求头%s'
                                '传参%s'
                                '返回体%s',
                                read_yaml('headers'),
                                info['parame'],
                                response)
        try:
            assert response['code'] == info['result']['code']
            assert response['msg'] == info['result']['msg']

        except AssertionError:
            logger.getlogger().error("inhos/measure/temp/list %s", "接口报错", exc_info=1)
            assert response['code'] == info['result']['code']
        logger.getlogger().info('---->接口:%s结束一次用例测试', url.format('inhos/measure/temp/list'))

    @allure.title('临时检测血糖修改')
    @pytest.mark.parametrize('info', yaml.safe_load(read_yaml_info(load('../data/path/path.yaml')['inhos_measure_temp_update'])))
    def test_temp_glu_update(self, info):
        logger.getlogger().info('---->接口:%s开始测试', url.format('inhos/measure/temp/update'))
        response = requests.post(url.format('inhos/measure/temp/update'), headers=read_yaml('headers'),
                                 data=json.dumps(info['parame'])).json()
        logger.getlogger().info('inhos/measure/temp/update：请求头%s'
                                '传参%s'
                                '返回体%s',
                                read_yaml('headers'),
                                info['parame'],
                                response)
        data = MysqlDb().select_db(
            "select * from {}.`blood_glucose_record` where id=\'{}\'".format(
                read_bastase_sql()[4],
                info['parame']['id'],

            ))

        try:
            assert data[0]['time_type'] == info['parame']['timeType']
            assert response['code'] == info['result']['code']
            assert response['msg'] == info['result']['msg']

        except AssertionError:
            logger.getlogger().error("inhos/measure/temp/update %s", "接口报错", exc_info=1)
            assert response['code'] == info['result']['code']
            assert data[0]['time_type'] == info['parame']['timeType']
        logger.getlogger().info('---->接口:%s结束一次用例测试', url.format('inhos/measure/temp/update'))

    @allure.title('临时检测血糖删除')
    @pytest.mark.parametrize('info', yaml.safe_load(read_yaml_info(load('../data/path/path.yaml')['inhos_measure_temp_delete'])))
    def test_temp_glu_del(self,info):
        info['parame']['id'] = str(int(info['parame']['id'])+1)
        logger.getlogger().info('---->接口:%s开始测试', url.format('inhos/measure/temp/delete'))
        response = requests.post(url.format('inhos/measure/temp/delete'), headers=read_yaml('headers'),
                                 data=json.dumps(info['parame'])).json()


        logger.getlogger().info('inhos_measure_temp_delete：请求头%s'
                                '传参%s'
                                '返回体%s',
                                read_yaml('headers'),
                                info['parame'],
                                response)

        data = MysqlDb().select_db(
            "select * from {}.`blood_glucose_record` where id=\'{}\'".format(
                read_bastase_sql()[4],
                info['parame']['id'],

            ))
        try:
            assert data[0]['status'] == 0
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("临时检测血糖删除 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
            assert data[0]['status'] == 0
