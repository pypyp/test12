import os
import sys

sys.path.append(r'' + os.path.abspath('../../'))
import allure
import pytest
import requests
from data.dev_info import dev
from testCase.log import logger
from common.yaml_util import read_yaml, read_zy_yaml, read_bastase_sql, read_url_csv
from common.open_database import MysqlDb
import json

url = read_url_csv()[0]
response = requests.post(url.format('device/list'), headers=read_yaml('headers'),
                         data=dev().dev_info()).json()
if response['data']['count'] == 0:
    requests.post(url.format('device/add/single'), headers=read_yaml('headers'),
                  data=dev().device_add()).json()

response = requests.post(url.format('device/list'), headers=read_yaml('headers'),
                         data=dev().dev_info()).json()

data1 = {
    'id': response['data']['lists'][0]["id"],
    "sn": response['data']['lists'][0]["sn"],
    'bindModule': response['data']['lists'][0]["bindModule"],
    "contrastTest": response['data']['lists'][0]["contrastTest"],
    "devQuality": response['data']['lists'][0]["devQuality"],
    "devStatus": response['data']['lists'][0]["devStatus"],
    "enableAdb": response['data']['lists'][0]["enableAdb"],
    "enableMtk": response['data']['lists'][0]["enableMtk"],
    "enableTouchFeedback": response['data']['lists'][0]["enableTouchFeedback"],
    "externalQuality": response['data']['lists'][0]["externalQuality"],
    "inhosDeptId": response['data']['lists'][0]["inhosDeptId"],
    "uploadMtk": response['data']['lists'][0]["uploadMtk"]
}

print(data1)

class Test_Liquid(object):

    @allure.title('编辑设备')
    @pytest.mark.run(order=1)
    def test_dev_update(self):
        logger.getlogger().info('测试的接口:%s', url.format('device/update'))
        data1['enableTouchFeedback'] = 1
        response = requests.post(url.format('device/update'), headers=read_yaml('headers'),
                                 data=json.dumps(data1)).json()

        data = MysqlDb().select_db(
            "select * from {}.`dev_info` where id =\'{}\'".format(read_bastase_sql()[4], data1['id']))
        logger.getlogger().info('编辑设备：传参%s返回体%s', data1, response)

        try:
            assert data[0]['enable_touch_feedback'] == data1['enableTouchFeedback']
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("编辑设备 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
            assert data[0]['enable_touch_feedback'] == data1['enableTouchFeedback']
    #
    @allure.title('删除设备')
    @pytest.mark.run(order=2)
    def test_dev_delete(self):
        logger.getlogger().info('测试的接口:%s', url.format('device/delete'))

        response = requests.post(url.format('device/delete'), headers=read_yaml('headers'),
                                 data=json.dumps({"id": data1['id']})).json()
        data = MysqlDb().select_db(
            "select * from {}.`dev_info` where id =\'{}\'".format(read_bastase_sql()[4], data1['id']))
        logger.getlogger().info('删除设备：传参%s返回体%s', data1['id'], response)

        try:
            assert data[0]['status'] == 0
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("删除设备 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
            assert data[0]['status'] == 0
    # #
    @allure.title('添加设备')
    @pytest.mark.run(order=3)
    @pytest.mark.parametrize('info', [dev().device_add()])
    def test_dev_add(self,info):
        logger.getlogger().info('测试的接口:%s', url.format('device/add/single'))
        response = requests.post(url.format('device/add/single'), headers=read_yaml('headers'),
                                 data=info).json()
        data = MysqlDb().select_db(
            "select * from {}.`dev_info` order by id desc".format(read_bastase_sql()[4]))
        logger.getlogger().info('添加设备：传参%s返回体%s', data1, response)

        try:
            assert data[0]['sn'] == json.loads(info)['sn']
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("添加设备 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
            assert data[0]['sn'] == json.loads(info)['sn']
    #
    @allure.title('查询设备')
    @pytest.mark.run(order=4)
    @allure.description('该接口写了3个用例全部，根据科室，sn，')
    @pytest.mark.parametrize('info', [dev().dev_select(),
                                      dev().dev_select1(),
                                      dev().dev_select_mh(),
                                      ])
    def test_dev_list(self, info):
        logger.getlogger().info('测试的接口:%s', url.format('device/list'))
        response = requests.post(url.format('device/list'), headers=read_yaml('headers'),
                                 data=info).json()

        logger.getlogger().info('查询设备：传参%s返回体%s', info, response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'

        except AssertionError:
            logger.getlogger().error("查询设备 %s", "接口报错", exc_info=1)
            assert response['code'] == 0



