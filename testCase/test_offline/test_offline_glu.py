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


@allure.feature("离线血糖")
class Test_offline_glu_1(object):
    @allure.title('离线添加血糖上传')
    @pytest.mark.run(order=1)
    def test_offline_glu_upload(self):
        logger.getlogger().info('测试的接口:%s', url.format('offline/inhos/measure/uploadMeasures'))
        response = requests.post(url.format('offline/inhos/measure/uploadMeasures'), headers=offilne.headers,
                      data=json.dumps(offline_glu.glu_upload())).json()
        logger.getlogger().debug('上传离线血糖：传参%s返回体%s', offline_glu.glu_upload(), response)

        for i in offline_glu.glu_upload()['measures']:
            data = MysqlDb().select_db(
                "select * from {}.`blood_glucose_record` where user_id =\'{}\' and measure_time =\'{}\'".format(read_bastase_sql()[4],
                                                                                       i['userId'],i['measureTime']))

            try:
                assert response['code'] == 0
                assert response['msg'] == '请求成功'
                assert data != []
            except AssertionError:
                logger.getlogger().error("上传离线血糖 %s", "接口报错", exc_info=1)
                assert response['code'] == 0
                assert data != []
        response = requests.post(url.format('offline/getSynInfo'), headers=offilne.headers,
                                 data=json.dumps(offilne.get_time())).json()


        assert response['data']['gluUpdated'] == 1
        print("---------离线血糖上传成功----------")

    @allure.title("离线血糖查询")
    @pytest.mark.run(order=2)
    def test_offline_glu_list(self):
        logger.getlogger().info('测试的接口:%s', url.format('offline/inhos/glu/measureGluList'))

        print("---------离线血糖查询开始----------")
        sql = """delete from glucose where type = 1 """
        sqlite().delete(sql)

        info = requests.post(url.format('offline/inhos/glu/measureGluList'), headers=offilne.headers, data=
        json.dumps({
            "updateTime": offilne.get_time()['gluUpdateTime'],
            "pageNo": 1,
            "pageSize": 500,
            "userIds": offilne.get_time()['userIds']
        })).json()
        logger.getlogger().info('离线血糖查询：传参%s返回体%s', {
            "updateTime": offilne.get_time()['gluUpdateTime'],
            "pageNo": 1,
            "pageSize": 500,
            "userIds": offilne.offline['userIds']
        }, info)
        for i in info['data']['lists']:
            try:
                userId = i['userId']
            except:
                userId = ''
            try:
                measureId = i['measureId']
            except:
                measureId = ''

            try:
                deptId = i['deptId']
            except:
                deptId = ''
            try:
                name = i['name']
            except:
                name = ''
            try:
                iptNum = i['iptNum']
            except:
                iptNum = ''
            try:
                bedNum = i['bedNum']
            except:
                bedNum = ''

            try:
                comment = i['bedSort']
            except:
                comment = ''

            try:
                bedSort = i['bedSort']
            except:
                bedSort = ''
            try:
                value = i['value']
            except:
                value = ''
            try:
                deviceNo = i['deviceNo']
            except:
                deviceNo = ''

            sql = """INSERT INTO "glucose"
                                    ("uid", "id", "measureId", "userId", "iptNum", "deptId", "name", "bedNum", "timeType", "timeSlot", "measureType", "value", "deviceNo", "method", "measureTime", "unusual", "nurseId", "nurseName", "valueUnit", "updateTime", "comment", "status", "type", "color", "bedSort")
                                    VALUES (NULL,\'{}\' , \'{}\', \'{}\', \'{}\',\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\',\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')""".format(
                i['id'], measureId, userId, iptNum, deptId, name,
                bedNum, i['timeType'], i['timeSlot'], i['measureType'], value,
                deviceNo, i['method'], i['measureTime'], i['unusual'], i['nurseId'],
                i['nurseName'], i['valueUnit'], i['updateTime'], comment, i['status'],
                0, 2, bedSort)
            try:
                sqlite().insert(sql)
                sql1 = """select id from glucose where id =\'{}\'""".format(i['id'])
                assert sqlite().select_id(sql1) != []
            except:
                logger.getlogger().debug('数据可能已经存在请查询sql%s',sql)
                assert sqlite().select_id(sql1) != []

@allure.feature("首次下拉离线血糖")
class Test_offline_glu_2(object):
    def test_offline_glu_list(self):
        logger.getlogger().info('测试的接口:%s', url.format('offline/inhos/glu/measureGluList'))
        print("---------离线血糖查询----------")
        sql = """delete from glucose"""
        sqlite().delete(sql)

        info = requests.post(url.format('offline/inhos/glu/measureGluList'), headers=offilne.headers, data=
        json.dumps({

            "pageNo": 1,
            "pageSize": 500,
            "userIds": []
        })).json()
        logger.getlogger().debug('离线血糖查询：传参%s返回体%s', {
            "pageNo": 1,
            "pageSize": 500,
            "userIds": []
        }, info)
        for i in info['data']['lists']:
            try:
                userId = i['userId']
            except:
                userId = ''
            try:
                measureId = i['measureId']
            except:
                measureId = ''

            try:
                deptId = i['deptId']
            except:
                deptId = ''
            try:
                name = i['name']
            except:
                name = ''
            try:
                iptNum = i['iptNum']
            except:
                iptNum = ''
            try:
                bedNum = i['bedNum']
            except:
                bedNum = ''

            try:
                comment = i['bedSort']
            except:
                comment = ''

            try:
                bedSort = i['bedSort']
            except:
                bedSort = ''
            try:
                value = i['value']
            except:
                value = ''
            try:
                deviceNo = i['deviceNo']
            except:
                deviceNo = ''

            sql = """INSERT INTO "glucose"
                                    ("uid", "id", "measureId", "userId", "iptNum", "deptId", "name", "bedNum", "timeType", "timeSlot", "measureType", "value", "deviceNo", "method", "measureTime", "unusual", "nurseId", "nurseName", "valueUnit", "updateTime", "comment", "status", "type", "color", "bedSort")
                                    VALUES (NULL,\'{}\' , \'{}\', \'{}\', \'{}\',\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\',\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')""".format(
                i['id'], measureId, userId, iptNum, deptId, name,
                bedNum, i['timeType'], i['timeSlot'], i['measureType'], value,
                deviceNo, i['method'], i['measureTime'], i['unusual'], i['nurseId'],
                i['nurseName'], i['valueUnit'], i['updateTime'], comment, i['status'],
                0, 2, bedSort)
            try:
                sqlite().insert(sql)
                sql1 = """select id from glucose where id =\'{}\'""".format(i['id'])
                assert sqlite().select_id(sql1) != []
            except:
                logger.getlogger().debug('数据可能已经存在请查询sql%s',sql)
                assert sqlite().select_id(sql1) != []


