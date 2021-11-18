# coding=UTF-8
import os
import sys

sys.path.append(r'' + os.path.abspath('../../'))
import pytest
import allure
import requests
from common.yaml_util import read_yaml, read_url_csv, read_bastase_sql, read_zy_yaml
from data.zy_temp_blood import zy_temp_blood
from testCase.log import logger
import json
from common.open_database import MysqlDb

url = read_url_csv()[0]


@allure.feature("临时检测血糖")
class Test_temp_blood():
    '''
    2条用例,一条没有关联患者，一条关联患者
    '''

    @allure.title('临时检测血糖添加')
    @pytest.mark.run(order=1)
    @allure.description('该接口写了2个用例添加临时检测，添加时绑定患者')
    @pytest.mark.parametrize('info', [zy_temp_blood().add_zy_temp_glu0(),
                                      zy_temp_blood().add_zy_temp_glu1()
                                      ])
    def test_add_temp_blood(self, info):
        logger.getlogger().info('测试的接口:%s', url.format('inhos/measure/temp/add'))
        response = requests.post(url.format('inhos/measure/temp/add'), headers=read_yaml('headers'),
                                 data=info).json()
        logger.getlogger().info('临时检测添加血糖信息：请求头%s传参%s返回体%s',
                                 read_yaml('headers'), info, response)

        data = MysqlDb().select_db(
            "select * from {}.`blood_glucose_record` where measure_time=\'{}\' and comment=\'{}\'".format(
                read_bastase_sql()[4],
                json.loads(info)['measureTime'],
                json.loads(info)['comment'],
            ))
        try:
            assert data[0] != {}
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("临时检测添加血糖 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
            assert data[0] != {}

    @allure.title('临时检测血糖修改')
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize('info', [zy_temp_blood().temp_glu_update0(),
                                      ])
    def test_temp_glu_update(self, info):
        logger.getlogger().info('测试的接口:%s', url.format('inhos/measure/temp/update'))
        response = requests.post(url.format('inhos/measure/temp/update'), headers=read_yaml('headers'),
                                 data=info).json()
        logger.getlogger().info('临时检测血糖修改：请求头%s传参%s返回体%s',
                                 read_yaml('headers'), info, response)

        data = MysqlDb().select_db(
            "select * from {}.`blood_glucose_record` where id=\'{}\'".format(
                read_bastase_sql()[4],
                json.loads(info)['id'],

            ))
        # print(data[0]['value'], json.loads(info)['value'])
        try:
            assert data[0]['time_type'] == json.loads(info)['timeType']
            # assert data[0]['value'] == json.loads(info)['value']
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("临时检测血糖修改 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
            assert data[0]['time_type'] == json.loads(info)['timeType']

    @allure.title('临时检测血糖值绑定患者')
    @pytest.mark.run(order=3)
    @pytest.mark.parametrize('info', [zy_temp_blood().temp_glu_update1(),
                                      ])
    def test_temp_glu_update_add(self, info):
        logger.getlogger().info('测试的接口:%s', url.format('inhos/measure/temp/update'))
        response = requests.post(url.format('inhos/measure/temp/update'), headers=read_yaml('headers'),
                                 data=info).json()
        logger.getlogger().info('临时检测血糖绑定患者：请求头%s传参%s返回体%s',
                                 read_yaml('headers'), info, response)

        data = MysqlDb().select_db(
            "select * from {}.`blood_glucose_record` where id=\'{}\'".format(
                read_bastase_sql()[4],
                json.loads(info)['id'],

            ))
        try:
            assert data[0]['measure_type'] == 1
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("临时检测血糖绑定患者 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
            assert data[0]['measure_type'] == 1

    @pytest.mark.run(order=4)
    @allure.title('临时检测血糖列表')
    @allure.description('该接口写了2个用例全部记录，根据时间筛选今天')
    @pytest.mark.parametrize('info', [zy_temp_blood().tmep_glu_list1(),
                                      zy_temp_blood().tmep_glu_list2()
                                      ])
    def test_temp_glu_list(self, info):
        logger.getlogger().info('测试的接口:%s', url.format('inhos/measure/temp/list'))
        response = requests.post(url.format('inhos/measure/temp/list'), headers=read_yaml('headers'),
                                 data=info).json()
        logger.getlogger().info('临时检测血糖列表：请求头%s传参%s返回体%s',
                                 read_yaml('headers'), info, response)

        try:

            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("临时检测血糖列表 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.title('临时检测血糖删除')
    @pytest.mark.run(order=4)
    def test_temp_glu_del(self):
        logger.getlogger().info('测试的接口:%s', url.format('inhos/measure/temp/delete'))
        data0 = MysqlDb().select_db(
            "select * from {}.`blood_glucose_record` where measure_type=\'{}\' order by id desc".format(
                read_bastase_sql()[4],
                0,

            ))
        id = data0[0]['id']
        response = requests.post(url.format('inhos/measure/temp/delete'), headers=read_yaml('headers'),
                                 data=json.dumps({"id": id})).json()
        logger.getlogger().info('临时检测血糖删除：请求头%s传参%s返回体%s',
                                 read_yaml('headers'), json.dumps({"id": id}), response)

        data = MysqlDb().select_db(
            "select * from {}.`blood_glucose_record` where id=\'{}\'".format(
                read_bastase_sql()[4],
                id,

            ))
        try:
            assert data[0]['status'] == 0
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("临时检测血糖删除 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
            assert data[0]['status'] == 0
