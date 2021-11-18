import os
import sys

sys.path.append(r'' + os.path.abspath('../../'))
import allure
import pytest
import requests
from data.liquid import liquid
from testCase.log import logger
from common.yaml_util import read_yaml, read_zy_yaml, read_bastase_sql, read_url_csv
from common.open_database import MysqlDb
import json

url = read_url_csv()[0]
response = requests.post(url.format('qc/liquid/list'), headers=read_yaml('headers'),
                         data=liquid().liquid_info()).json()
if response['data']['count'] == 0:
    requests.post(url.format('qc/liquid/add/single'), headers=read_yaml('headers'),
                  data=liquid().liquid_add()).json()

response = requests.post(url.format('qc/liquid/list'), headers=read_yaml('headers'),
                         data=liquid().liquid_info()).json()
data1 = {
    'id': response['data']['lists'][0]["id"],
    "specs": response['data']['lists'][0]["specs"],
    'type': response['data']['lists'][0]["type"],
    "liquidNum": response['data']['lists'][0]["liquidNum"],
    "productionDate": response['data']['lists'][0]["productionDate"],
    "expiryDate": response['data']['lists'][0]["expiryDate"],
    "batchNum": response['data']['lists'][0]["batchNum"]
}
print(data1)

class Test_Liquid(object):

    @allure.title('编辑质控液')
    @pytest.mark.run(order=1)
    def test_liquid_update(self):
        logger.getlogger().info('测试的接口:%s', url.format('qc/liquid/update'))
        data1['type'] = 1
        response = requests.post(url.format('qc/liquid/update'), headers=read_yaml('headers'),
                                 data=json.dumps(data1)).json()
        data = MysqlDb().select_db(
            "select * from {}.`qc_liquid_info` where id =\'{}\'".format(read_bastase_sql()[4], data1['id']))
        logger.getlogger().info('编辑质控液：传参%s返回体%s', data1, response)

        try:
            assert data[0]['type'] == data1['type']
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("编辑质控液 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
            assert data[0]['type'] == data1['type']

    @allure.title('删除质控液')
    @pytest.mark.run(order=2)
    def test_liquid_del(self):
        logger.getlogger().info('测试的接口:%s', url.format('qc/liquid/delete'))
        response = requests.post(url.format('qc/liquid/delete'), headers=read_yaml('headers'),
                                 data=json.dumps({"id": data1['id']})).json()
        data = MysqlDb().select_db(
            "select * from {}.`qc_liquid_info` where id =\'{}\'".format(read_bastase_sql()[4],data1['id']))
        logger.getlogger().info('删除质控液：传参%s返回体%s', {"id": data1['id']}, response)

        try:
            assert data[0]['status'] == 0
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("删除质控液 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
            assert data[0]['status'] == 0

    @allure.title('添加质控液')
    @pytest.mark.run(order=3)
    @pytest.mark.parametrize('info', [liquid().liquid_add()])
    def test_liquid_add(self, info):
        logger.getlogger().info('测试的接口:%s', url.format('qc/liquid/add/single'))
        response = requests.post(url.format('qc/liquid/add/single'), headers=read_yaml('headers'),
                                 data=info).json()
        data = MysqlDb().select_db(
            "select * from {}.`qc_liquid_info` order by id desc".format(read_bastase_sql()[4]))
        logger.getlogger().info('添加质控液：传参%s返回体%s', info, response)

        try:
            assert data[0]['batch_num'] == json.loads(info)['batchNum']
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("添加质控液 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
            assert data[0]['batch_num'] == json.loads(info)['batchNum']

    @allure.title('查询质控液')
    @pytest.mark.run(order=4)
    @pytest.mark.parametrize('info', [liquid().liquid_select(),
                                      liquid().liquid_select_mh()])
    def test_liquid_list(self, info):
        logger.getlogger().info('测试的接口:%s', url.format('qc/liquid/list'))
        response = requests.post(url.format('qc/liquid/list'), headers=read_yaml('headers'),
                                 data=info).json()

        logger.getlogger().info('查询质控液：传参%s返回体%s', info, response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'

        except AssertionError:
            logger.getlogger().error("查询设备 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
