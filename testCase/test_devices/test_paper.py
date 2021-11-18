import os
import sys

sys.path.append(r'' + os.path.abspath('../../'))
import allure
import pytest
import requests
from data.paper import paper_info
from testCase.log import logger
from common.yaml_util import read_yaml, read_zy_yaml, read_bastase_sql, read_url_csv
from common.open_database import MysqlDb
import json

url = read_url_csv()[0]
response = requests.post(url.format('paper/list'), headers=read_yaml('headers'),
                         data=paper_info().paper_info()).json()
if response['data']['count'] == 0:
    requests.post(url.format('paper/add/single'), headers=read_yaml('headers'),
                  data=paper_info().paper_add()).json()
    print(1)
response = requests.post(url.format('paper/list'), headers=read_yaml('headers'),
                         data=paper_info().paper_info()).json()
data1 = {
    'id': response['data']['lists'][0]["id"],
    "specs": response['data']['lists'][0]["specs"],
    "paperNum": response['data']['lists'][0]["paperNum"],
    "productionDate": response['data']['lists'][0]["productionDate"],
    "expiryDate": response['data']['lists'][0]["expiryDate"],
    "lowMaxLimit": response['data']['lists'][0]["lowMaxLimit"],
    "lowMinLimit": response['data']['lists'][0]["lowMinLimit"],
    "mediumMaxLimit": response['data']['lists'][0]["mediumMaxLimit"],
    "mediumMinLimit": response['data']['lists'][0]["mediumMinLimit"],
    "highMaxLimit": response['data']['lists'][0]["highMaxLimit"],
    "highMinLimit": response['data']['lists'][0]["highMinLimit"],
    "batchNum": response['data']['lists'][0]["batchNum"]
}
print(data1)

class Test_paper(object):

    @allure.title('编辑试纸')
    @pytest.mark.run(order=1)
    def test_paper_update(self):
        logger.getlogger().info('测试的接口:%s', url.format('paper/update'))
        data1['paperNum'] = 100
        data1['specs'] = 1
        response = requests.post(url.format('paper/update'), headers=read_yaml('headers'),
                                 data=json.dumps(data1)).json()
        print(dict)
        data = MysqlDb().select_db(
            "select * from {}.`paper_info` where id =\'{}\'".format(read_bastase_sql()[4], data1['id']))
        logger.getlogger().info('编辑试纸：传参%s返回体%s', data1, response)

        try:
            assert data[0]['paper_num'] == data1['paperNum']
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("编辑试纸 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
            assert data[0]['paper_num'] == data1['paperNum']

    @allure.title('删除试纸')
    @pytest.mark.run(order=2)
    def test_paper_del(self):
        logger.getlogger().info('测试的接口:%s', url.format('paper/delete'))
        response = requests.post(url.format('paper/delete'), headers=read_yaml('headers'),
                                 data=json.dumps({"id": data1['id']})).json()
        data = MysqlDb().select_db(
            "select * from {}.`paper_info` where id =\'{}\'".format(read_bastase_sql()[4],data1['id']))
        logger.getlogger().info('删除试纸：传参%s返回体%s', {"id": data1['id']}, response)

        try:
            assert data[0]['status'] == 0
            assert response['code'] == 1
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("删除试纸 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
            assert data[0]['status'] == 0

    @allure.title('添加试纸')
    @pytest.mark.run(order=3)
    @pytest.mark.parametrize('info', [paper_info().paper_add()])
    def test_paper_add(self, info):
        logger.getlogger().info('测试的接口:%s', url.format('paper/add/single'))
        response = requests.post(url.format('paper/add/single'), headers=read_yaml('headers'),
                                 data=info).json()
        data = MysqlDb().select_db(
            "select * from {}.`paper_info` order by id desc".format(read_bastase_sql()[4]))
        logger.getlogger().info('添加试纸：传参%s返回体%s', info, response)

        try:
            assert data[0]['batch_num'] == json.loads(info)['batchNum']
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("添加试纸 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
            assert data[0]['batch_num'] == json.loads(info)['batchNum']

    @allure.title('查询试纸')
    @pytest.mark.run(order=4)
    @pytest.mark.parametrize('info', [paper_info().paper_select(),
                                      paper_info().paper_select_mh()])
    def test_paper_list(self, info):
        logger.getlogger().info('测试的接口:%s', url.format('paper/list'))
        response = requests.post(url.format('paper/list'), headers=read_yaml('headers'),
                                 data=info).json()
        logger.getlogger().info('添加试纸：传参%s返回体%s', info, response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'

        except AssertionError:
            logger.getlogger().error("查询设备 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
        # if "batchNum" in info:
        #     data = MysqlDb().select_db(
        #         "select count(*) from {}.`paper_info` where `status`='1' and hos_id=\'{}\' "
        #         "and batch_num LIKE '%20%'".format(read_bastase_sql()[4], read_yaml('hosId')))
        #     logger.getlogger().debug('查询试纸：传参%s返回体%s', info, response)
        #     # print(data[0],response['data']['totalCount'])
        #     try:
        #         assert data[0]['count(*)'] == response['data']['totalCount']
        #         assert response['code'] == 0
        #         assert response['msg'] == '请求成功'
        #     except AssertionError:
        #         logger.getlogger().error("查询试纸 %s", "接口报错", exc_info=1)
        #         assert response['code'] == 0
        #         assert data[0]['count(*)'] == response['data']['totalCount']
        #
        # else:
        #     data = MysqlDb().select_db(
        #         "select count(*) from {}.`paper_info` where `status`='1'  and hos_id=\'{}\'".format(
        #             read_bastase_sql()[4], read_yaml('hosId')))
        #     logger.getlogger().debug('查询试纸：传参%s返回体%s', info, response)
        #     # print(data[0],response['data']['totalCount'])
        #     try:
        #         assert data[0]['count(*)'] == response['data']['totalCount']
        #         assert response['code'] == 0
        #         assert response['msg'] == '请求成功'
        #     except AssertionError:
        #         logger.getlogger().error("查询试纸 %s", "接口报错", exc_info=1)
        #         assert response['code'] == 0
        #         assert data[0]['count(*)'] == response['data']['totalCount']
