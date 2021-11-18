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


@allure.feature("离线医护人员")
class Test_offline_user(object):
    @allure.title('离线医护人员')
    @pytest.mark.run(order=1)

    def test_offline_user(self):
        logger.getlogger().info('测试的接口:%s', url.format('offline/common/staff/list'))
        print("---------离线医护人员查询----------")
        sql = """delete from user """
        sqlite().delete(sql)
        response = requests.post(url.format('offline/common/staff/list'), headers=offilne.headers, data=
        json.dumps({
            "pageNo": -1,
            "pageSize": 20
        })).json()
        logger.getlogger().info('离线医护人员：传参%s返回体%s', {
            "pageNo": -1,
            "pageSize": 20
        }, response)
        for i in response['data']:
            try:
                gender = i['gender']
            except:
                gender = ''
            try:
                dataAuthIds = i['dataAuthIds']
            except:
                dataAuthIds = ''
            try:
                permissions = i['permissions']
            except:
                permissions = ''
            sql = """INSERT
                       INTO "user"("userId", "name", "gender", "keywords", "hisId", "deptId", "deptName", "saltToken", "password",
                              "dataAuthIds", "type", "permissions", "accessToken", "refreshToken", "isLogin", "lastLoginTime",
                              "remember")
                       VALUES(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\',
                              \'{}\', \'{}\', \'{}\', \'{}\',
                              NULL, NULL, NULL, NULL, 0)""".format(i['userId'], i["name"], gender, i['keywords'],
                                                                   i['hisId'], i['deptId'], i['deptName'],
                                                                   i['saltToken'],
                                                                   i['password'], dataAuthIds, i['type'], permissions)
            sqlite().insert(sql)
        sql ="select count(*) from user"

        assert sqlite().select_id(sql)[0][0] == len(response['data'])
