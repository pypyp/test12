import os
import sys

sys.path.append(r'' + os.path.abspath('../../'))
import allure
import pytest
import requests
from data.qc_record import qc_record
from testCase.log import logger
from common.yaml_util import read_yaml, read_zy_yaml, read_bastase_sql, read_url_csv
from common.open_database import MysqlDb
import json

url = read_url_csv()[0]
liquid_id = requests.post(url.format('qc/liquid/list'), headers=read_yaml('headers'),
                         data=qc_record().qc_record()).json()['data']['lists'][0]["id"]

paper_id = requests.post(url.format('paper/list'), headers=read_yaml('headers'),
                         data=qc_record().qc_record()).json()['data']['lists'][0]["id"]


response = requests.post(url.format('qc/record/list'), headers=read_yaml('headers'),
                         data=qc_record().qc_record()).json()

qc = qc_record().qc_add()
qc['paperId'] = paper_id
qc['liquidId'] = liquid_id
print(qc)
if response['data']['count'] == 0:

    requests.post(url.format('qc/record/add'), headers=read_yaml('headers'),
                  data=json.dumps(qc))


response = requests.post(url.format('qc/record/list'), headers=read_yaml('headers'),
                     data=qc_record().qc_record()).json()
print(response)
data1 = {
    'id': response['data']['lists'][0]["id"],
    "paperId": response['data']['lists'][0]["paperId"],
    'result': response['data']['lists'][0]["result"],
    "liquidId": response['data']['lists'][0]["liquidId"],
    "measureTime": response['data']['lists'][0]["measureTime"],
    "sn": response['data']['lists'][0]["sn"],
    "value": response['data']['lists'][0]["value"],
}

@allure.feature("质控")
class Test_qc_record(object):

    @allure.title('编辑质控')
    @pytest.mark.run(order=1)
    def test_qc_update(self):
        logger.getlogger().info('测试的接口:%s', url.format('qc/record/update'))
        data1['value'] = 8
        response = requests.post(url.format('qc/record/update'), headers=read_yaml('headers'),
                                 data=json.dumps(data1)).json()
        data = MysqlDb().select_db(
            "select * from {}.`qc_record` where id =\'{}\'".format(read_bastase_sql()[4], data1['id']))
        logger.getlogger().info('编辑质控：传参%s返回体%s', data1, response)

        try:
            assert data[0]['value'] == data1['value']
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("编辑质控 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
            assert data[0]['value'] == data1['value']

    @allure.title('删除质控')
    @pytest.mark.run(order=2)
    def test_qc_del(self):
        logger.getlogger().info('测试的接口:%s', url.format('qc/record/delete'))
        response = requests.post(url.format('qc/record/delete'), headers=read_yaml('headers'),
                                 data=json.dumps({"id": data1['id']})).json()
        data = MysqlDb().select_db(
            "select * from {}.`qc_record` where id =\'{}\'".format(read_bastase_sql()[4],data1['id']))
        logger.getlogger().info('删除质控液：传参%s返回体%s', {"id": data1['id']}, response)

        try:
            assert data[0]['status'] == 0
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("删除质控液 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
            assert data[0]['status'] == 0
#
    @allure.title('添加质控')
    @pytest.mark.run(order=3)
    @pytest.mark.parametrize('info', [json.dumps(qc)])
    def test_qc_add(self, info):
        logger.getlogger().info('测试的接口:%s', url.format('qc/record/add'))
        response = requests.post(url.format('qc/record/add'), headers=read_yaml('headers'),
                                 data=info).json()
        data = MysqlDb().select_db(
            "select * from {}.`qc_record` order by id desc".format(read_bastase_sql()[4]))
        logger.getlogger().info('添加质控：传参%s返回体%s', info, response)

        try:
            assert data[0]['value'] == json.loads(info)['value']
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("添加质控 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
            assert data[0]['value'] == json.loads(info)['value']

    @allure.title('查询质控')
    @pytest.mark.run(order=4)
    @allure.description('该接口写了4个用例添加全部，根据sn，根据浓度，根据，结果')
    @pytest.mark.parametrize('info', [qc_record().qc_select(),
                                      qc_record().qc_select1(),
                                      qc_record().qc_select2(),
                                      qc_record().qc_select3()
                                      ])
    def test_qc_list(self, info):
        logger.getlogger().info('测试的接口:%s', url.format('qc/record/list'))
        response = requests.post(url.format('qc/record/list'), headers=read_yaml('headers'),
                                 data=info).json()
        logger.getlogger().info('查询质控：传参%s返回体%s', info, response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("查询质控 %s", "接口报错", exc_info=1)
            assert response['code'] == 0



