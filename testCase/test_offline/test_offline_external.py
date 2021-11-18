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

@allure.feature("离线室间质评")
class Test_offline_external(object):
    @allure.title('离线室间质评上传')
    @pytest.mark.run(order=1)

    def test_offline_external_add(self):
        logger.getlogger().info('测试的接口:%s', url.format('offline/qc/external/add'))
        response = requests.post(url.format('offline/qc/external/add'), headers=offilne.headers,
                      data=json.dumps(offline_glu.external_upload())).json()
        logger.getlogger().debug('室间质评上传：传参%s返回体%s', offline_glu.external_upload(), response)

        for i in offline_glu.external_upload():
            data = MysqlDb().select_db(
                "select * from {}.`external_quality_control` where value =\'{}\' and measure_time =\'{}\'".format(
                    read_bastase_sql()[4],
                    i['value'], i['measureTime']))
            try:
                assert response['code'] == 0
                assert response['msg'] == '请求成功'
                assert data!=[]
            except AssertionError:
                logger.getlogger().error("上传离线室间质评 %s", "接口报错", exc_info=1)
                assert response['code'] == 0
                assert data != []

        response = requests.post(url.format('offline/getSynInfo'), headers=offilne.headers, data=json.dumps(offilne.get_time())).json()

        assert response['data']['externalUpdated'] == 1
        print("---------离线室间质评上传结束----------")
    @allure.title("离线室间质评查询")
    @pytest.mark.run(order=2)

    def test_offline_external_list(self):
        logger.getlogger().info('测试的接口:%s', url.format('offline/qc/external/list'))
        print("---------离线室间质评查询----------")
        sql = """delete from external_quality_assessment """
        sqlite().delete(sql)
        info = requests.post(url.format('offline/qc/external/list'), headers=offilne.headers, data=
        json.dumps({
        })).json()
        logger.getlogger().debug('离线室间质评查询：传参%s返回体%s', {}, info)

        for i in info['data']:
            sql = """INSERT INTO
            "external_quality_assessment"("uid", "id", "sn", "measureTime", "batchNum", "sampleNum", "value", "nurseId", "type")
            VALUES(NULL, \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', 0)""".format(
                i['id'], i["sn"], i["measureTime"], i["batchNum"], i["sampleNum"], i["value"], i["nurseId"]
            )
            sqlite().insert(sql)
        sql = 'select count(*) from external_quality_assessment'
        assert sqlite().select_id(sql)[0][0] == len(info['data'])

        # sql = """UPDATE common_update_time
        #                                                             SET externalUpdateTime = \'{}\' WHERE id =1
        #                                                           """.format(time1)
        # sqlite().sqlite_update_time(sql)
