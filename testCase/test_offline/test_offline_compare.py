import os
import sys

sys.path.append(r'' + os.path.abspath('../../'))
import allure
import pytest
import requests
from data import offline_glu
from testCase.log import logger
from common.yaml_util import read_url_csv, read_bastase_sql
from testCase import offilne
from common.open_database import MysqlDb
from testCase.offline_basic.sqlite import sqlite
import json,time

url = read_url_csv()[1]

@allure.feature("离线对比测试")
class Test_offline_compare(object):
    @allure.title('离线对比测试上传')
    @pytest.mark.run(order=1)
    def test_offline_compare_upload(self):
        logger.getlogger().info('测试的接口:%s', url.format('offline/cp/uploadRecords'))
        response = requests.post(url.format('offline/cp/uploadRecords'), headers=offilne.headers,
                      data=json.dumps(offline_glu.compare_upload())).json()
        logger.getlogger().debug('对比测试上传：传参%s返回体%s', offline_glu.compare_upload(), response)
        for i in offline_glu.compare_upload():
            data = MysqlDb().select_db(
                "select * from {}.`comparison_manage` where result =\'{}\' and detection_time =\'{}\'".format(
                    read_bastase_sql()[4],
                    i['result'], i['detectionTime']))
            try:
                assert response['code'] == 0
                assert response['msg'] == '请求成功'
                assert data != []
            except AssertionError:
                logger.getlogger().error("上传离线对比测试 %s", "接口报错", exc_info=1)
                assert response['code'] == 0
                assert data != []

        response = requests.post(url.format('offline/getSynInfo'), headers=offilne.headers,
                                 data=json.dumps(offilne.get_time())).json()

        assert response['data']['comparisonUpdated'] == 1
        print("---------离线对比测试上传成功----------")
    @allure.title("对比测试查询")
    @pytest.mark.run(order=2)

    def test_offline_compare_list(self):
        logger.getlogger().info('测试的接口:%s', url.format('offline/cp/list'))
        print("---------离线对比查询----------")
        sql = """delete from compare_test_record """
        sqlite().delete(sql)
        info = requests.post(url.format('offline/cp/list'), headers=offilne.headers, data=
        json.dumps({
        })).json()

        logger.getlogger().debug('对比测试查询：传参%s返回体%s', {}, info)
        for i in info['data']['lists']:
            try:
                operatorUserId = i['operatorUserId']
            except:
                operatorUserId = ''
            sql = """INSERT INTO
                "compare_test_record"("uid", "id", "result", "unusual", "detectionTime", "paperId", "paperBatchNum",
                                      "operatorUserId", "sampleNo", "status", "remote")
                VALUES(NULL, \'{}\', \'{}\', \'{}\',\'{}\' , \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', 1)""".format(
                i['id'], i['result'], i['unusual'], i['detectionTime'], '', i['paperBatchNum'],
                operatorUserId, i['sampleNo'], i['status']
            )
            sqlite().insert(sql)
        sql = 'select count(*) from compare_test_record'
        assert sqlite().select_id(sql)[0][0] == info['data']['count']
