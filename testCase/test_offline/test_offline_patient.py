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


@allure.feature("离线患者")
class Test_offline_patient(object):
    @allure.title('离线患者更新')
    @pytest.mark.run(order=1)

    def test_offline_patient(self):
        logger.getlogger().info('测试的接口:%s', url.format('offline/inhos/patient/list'))
        print("---------离线患者查询----------")
        time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """delete from patient """
        sqlite().delete(sql)
        try:
            userIds = offilne.get_time()['userIds']
        except:
            userIds = []
        info = requests.post(url.format('offline/inhos/patient/list'), headers=offilne.headers, data=
        json.dumps({
            "pageNo": -1,
            "pageSize": 20,
            "userIds": userIds
        })).json()
        logger.getlogger().debug('离线患者：传参%s返回体%s', {
            "pageNo": -1,
            "pageSize": 20,
            "userIds": userIds
        }, info)

        for i in info['data']['lists']:
            try:
                bedNum = i['bedNum']
            except:
                bedNum = ''
            try:
                birthday = i['birthday']
            except:
                birthday = ''
            try:
                primayDocId = i['primayDocId']
            except:
                primayDocId = ''
            try:
                primayDocName = i['primayDocName']
            except:
                primayDocName = ''
            try:
                primayNurseId = i['primayNurseId']
            except:
                primayNurseId = ''
            try:
                phone = i['phone']
            except:
                phone = ''

            try:
                bedSort = i['bedSort']
            except:
                bedSort = ''

            sql = """INSERT INTO
            "patient"("userId", "iptNum", "name", "gender", "bedNum", "birthday", "deptId", "deptName", "primayDocId",
                      "primayDocName", "primayNurseId", "iptTime", "primayType", "phone", "bedSort")
            VALUES(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\',
                   \'{}\', NULL, \'{}\', \'{}\')""". \
                format(i['userId'], i['iptNum'], i['name'], i['gender'], bedNum, birthday, i['deptId'], i['deptName'],
                       primayDocId, primayDocName, primayNurseId, i["iptTime"], phone, bedSort)
            sqlite().insert(sql)
        sql = 'select count(*) from patient'
        assert sqlite().select_id(sql)[0][0] == info['data']['totalCount']

