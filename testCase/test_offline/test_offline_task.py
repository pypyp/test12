import os
import sys

sys.path.append(r'' + os.path.abspath('../../'))
import allure
import pytest
import time
import requests
from data import offline_glu
from testCase.log import logger
from common.yaml_util import read_url_csv
from testCase import offilne
from testCase.offline_basic.sqlite import sqlite
import json

url = read_url_csv()[1]


@allure.feature("离线医嘱")
class Test_offline_task(object):
    @allure.title('离线医嘱更新')
    def test_offline_task_0(self):
        logger.getlogger().info('测试的接口:%s',url.format('offline/inhos/glu_order/monitorList'))
        print("---------离线医嘱查询----------")
        sql = """delete from task """
        sqlite().delete(sql)
        try:
            userIds = offilne.get_time()['userIds']
        except:
            userIds = []
        info = requests.post(url.format('offline/inhos/glu_order/monitorList'), headers=offilne.headers, data=
        json.dumps({
            "pageNo": -1,
            "pageSize": 20,
            "userIds": userIds
        })).json()
        try:
            task =info['data']['tasks']
        except:
            task = ''
        logger.getlogger().info('医嘱查询：传参%s返回体%s', userIds, info)

        if task != '':
            for i in info['data']['tasks']:
                try:
                    bedNum = i['bedNum']
                except:
                    bedNum = ''
                try:
                    entrust = i['entrust']
                except:
                    entrust = ''

                try:
                    endTime = i['endTime']
                except:
                    endTime = ''

                try:
                    orderEndTime = i['orderEndTime']
                except:
                    orderEndTime = ''

                try:
                    orderId = i['orderId']
                except:
                    orderId = ''
                try:
                    bedSort = i['bedSort']
                except:
                    bedSort = ''
                sql = """INSERT INTO
                "task"("id", "userId", "iptNum", "deptId", "name", "bedNum", "timeType", "entrust", "type", "docId", "docName", "startTime", "endTime", "orderStartTime", "orderEndTime", "execNum", "testNum", "orderId", "reminderId", "reminderTime", "close", "bedSort")
                VALUES (NULL, \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', NULL, '', 0, \'{}\')""".format(
                    i['userId'], i["iptNum"], i['deptId'], i['name'], bedNum, i['timeType'], entrust, i['type'],
                    i['docId'], i['docName'], i['startTime'], endTime, i["orderStartTime"], orderEndTime,
                    i["analysisExecNum"], i['analysisTestNum'], orderId, bedSort
                )
                sqlite().insert(sql)
            sql ='select count(*) from task'
            assert len(info['data']['tasks'])==sqlite().select_id(sql)[0][0]
        else:
            logger.getlogger().info('没有医嘱')



    def test_offline_task_1(self):
        logger.getlogger().info('测试的接口:%s', url.format('offline/inhos/glu_order/monitorList'))
        print("---------离线医嘱查询----------")
        sql = """delete from analysis_task """
        sqlite().delete(sql)
        try:
            userIds = offilne.get_time()['userIds']
        except:
            userIds = []
        info = requests.post(url.format('offline/inhos/glu_order/monitorList'), headers=offilne.headers, data=
        json.dumps({
            "pageNo": -1,
            "pageSize": 20,
            "userIds": userIds
        })).json()
        logger.getlogger().debug('医嘱查询：传参%s返回体%s', userIds, info)
        try:
            taskLookupList = info['data']['tasks']
        except:
            taskLookupList = ''
        if taskLookupList != '':
            for j in info['data']['taskLookupList']:

                for i in j['tasks']:

                    try:
                        bedNum = i['bedNum']
                    except:
                        bedNum = ''
                    try:
                        entrust = i['entrust']
                    except:
                        entrust = ''

                    try:
                        endTime = i['endTime']
                    except:
                        endTime = ''

                    try:
                        orderEndTime = i['orderEndTime']
                    except:
                        orderEndTime = ''

                    try:
                        filterTimeType = i['filterTimeType']
                    except:
                        filterTimeType = ''

                    try:
                        bedSort = i['filterTimeType']
                    except:
                        bedSort = ''
                    sql = """INSERT INTO
                    "analysis_task"("id", "uId", "userId", "iptNum", "name", "testNum", "execNum", "docId", "docName", "deptId", "type", "startTime", "endTime", 
                    "timeType", "orderStartTime","orderEndTime", "analysisTestNum", "analysisExecNum", "showType", "analysisTimeType", "analysisTimeSlot", "reminderId", 
                    "reminderTime", "orderId", "filterTimeType", "bedNum", "close", "bedSort", "entrust")
                    VALUES (NULL, \'{}\', \'{}\',\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\',\'{}\',\'{}\', '', '',\'{}\',\'{}\',\'{}\', 0, \'{}\',\'{}\')""".format(
                        i['id'], i['userId'], i["iptNum"], i['name'], i['testNum'], i['execNum'], i['docId'], i['docName'],
                        i['deptId'], i['type'], i['startTime'], endTime, i['timeType'],i['orderStartTime'],orderEndTime,
                        i['analysisTestNum'],i['analysisExecNum'],i['showType'],i['analysisTimeType'],i['analysisTimeSlot'],i['orderId'],
                        filterTimeType, bedNum, bedSort,entrust
                    )
                    sqlite().insert(sql)
            sql = 'select count(*) from analysis_task'
            assert len(info['data']['taskLookupList']) == sqlite().select_id(sql)[0][0]
        else:
            logger.getlogger().info('没有医嘱')
