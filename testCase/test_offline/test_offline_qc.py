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
import json, time

url = read_url_csv()[1]


@allure.feature("离线质控")
class Test_offline_qc_1(object):
    @allure.title('离线质控上传')
    @pytest.mark.run(order=1)
    def test_offline_qc_upload(self):
        logger.getlogger().info('测试的接口:%s', url.format('offline/qc/record/uploadRecords'))
        response = requests.post(url.format('offline/qc/record/uploadRecords'), headers=offilne.headers,
                                 data=json.dumps(offline_glu.qc_upload())).json()
        logger.getlogger().debug('质控上传：传参%s返回体%s', offline_glu.qc_upload(), response)
        for i in offline_glu.qc_upload():
            data = MysqlDb().select_db(
                "select * from {}.`qc_record` where value =\'{}\' and measure_time =\'{}\'".format(
                    read_bastase_sql()[4],
                    i['value'], i['measureTime']))
            try:
                assert response['code'] == 0
                assert response['msg'] == '请求成功'
                assert data != []
            except AssertionError:
                logger.getlogger().error("上传质控 %s", "接口报错", exc_info=1)
                assert response['code'] == 0
                assert data != []

        response = requests.post(url.format('offline/getSynInfo'), headers=offilne.headers,
                                 data=json.dumps(offilne.get_time())).json()

        assert response['data']['qcRecordUpdated'] == 1
        print("---------离线质控上传结束----------")
    @allure.title("离线质控查询")
    @pytest.mark.run(order=2)
    def test_offline_qc_list(self):
        logger.getlogger().info('测试的接口:%s', url.format('offline/qc/record/list'))
        print("---------离线质控查询开始----------")
        sql = """delete from quality_control where remote = 1 """
        sqlite().delete(sql)
        info = requests.post(url.format('offline/qc/record/list'), headers=offilne.headers, data=json.dumps({
            "updateTime": offilne.get_time()['qcRecordUpdateTime'],
            "pageNo": 1,
            "pageSize": 500,
        })).json()

        logger.getlogger().debug('质控查询：传参%s返回体%s', {"updateTime": offilne.get_time()['qcRecordUpdateTime'],
                                                      "pageNo": 1,
                                                      "pageSize": 500,
                                                      }, info)
        for i in info['data']['lists']:
            try:
                paperOpenTime = i["paperOpenTime"]
            except:
                paperOpenTime = ''
            try:
                liquidOpenTime = i["liquidOpenTime"]
            except:
                liquidOpenTime = ''

            sql = """INSERT INTO
                            "quality_control"("uid", "id", "value", "sn", "result", "measureTime", "operatorUserName", "operatorUserId",
                                              "deptId", "deptName", "paperId", "paperOpenTime", "paperBatchNum", "paperProductionDate",
                                              "paperExpiryDate", "liquidId", "liquidBatchNum", "liquidOpenTime", "liquidProductionDate",
                                              "liquidExpiryDate", "type", "low", "high", "remote", "status")
                            VALUES(NULL, \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', '', '', \'{}\', \'{}\', \'{}\', \'{}\',
                                   \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')""". \
                format(i['id'], i['value'], i['sn'], i['result'], i['measureTime'], i['operatorUserName'],
                       i['deptName'], i['paperId'],
                       paperOpenTime, i["paperBatchNum"], i['paperProductionDate'], i['paperExpiryDate'],
                       i['liquidId'],
                       i['liquidBatchNum'],
                       liquidOpenTime, i['liquidProductionDate'], i['liquidExpiryDate'], i['type'], i["low"],
                       i["high"],
                       0, i['status'])
            try:
                sqlite().insert(sql)
                sql1 = """select id from quality_control where id =\'{}\'""".format(i['id'])
                assert sqlite().select_id(sql1) != []
            except:
                logger.getlogger().debug('数据可能已经存在请查询sql%s', sql)
                assert sqlite().select_id(sql1) != []



@allure.feature("首次下拉离线质控")
class Test_offline_qc_2(object):
    def test_offline_qc_list(self):
        logger.getlogger().info('测试的接口:%s', url.format('offline/qc/record/list'))
        print("---------离线质控查询开始----------")
        sql = """delete from quality_control """
        sqlite().delete(sql)

        info = requests.post(url.format('offline/qc/record/list'), headers=offilne.headers, data=json.dumps({

            "pageNo": 1,
            "pageSize": 500,
        })
                             ).json()

        logger.getlogger().debug('上传质控上传：传参%s返回体%s', {

            "pageNo": 1,
            "pageSize": 500,
        }, info)
        for i in info['data']['lists']:
            try:
                paperOpenTime = i["paperOpenTime"]
            except:
                paperOpenTime = ''
            try:
                liquidOpenTime = i["liquidOpenTime"]
            except:
                liquidOpenTime = ''

            sql = """INSERT INTO
                                    "quality_control"("uid", "id", "value", "sn", "result", "measureTime", "operatorUserName", "operatorUserId",
                                                      "deptId", "deptName", "paperId", "paperOpenTime", "paperBatchNum", "paperProductionDate",
                                                      "paperExpiryDate", "liquidId", "liquidBatchNum", "liquidOpenTime", "liquidProductionDate",
                                                      "liquidExpiryDate", "type", "low", "high", "remote", "status")
                                    VALUES(NULL, \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', '', '', \'{}\', \'{}\', \'{}\', \'{}\',
                                           \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')""". \
                format(i['id'], i['value'], i['sn'], i['result'], i['measureTime'], i['operatorUserName'],
                       i['deptName'], i['paperId'],
                       paperOpenTime, i["paperBatchNum"], i['paperProductionDate'], i['paperExpiryDate'],
                       i['liquidId'],
                       i['liquidBatchNum'],
                       liquidOpenTime, i['liquidProductionDate'], i['liquidExpiryDate'], i['type'], i["low"],
                       i["high"],
                       0, i['status'])
            try:
                sqlite().insert(sql)
                sql1 = """select id from quality_control where id =\'{}\'""".format(i['id'])
                assert sqlite().select_id(sql1) != []
            except:
                logger.getlogger().debug('数据可能已经存在请查询sql%s', sql)
                assert sqlite().select_id(sql1) != []