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


@allure.feature("离线试纸质控液")
class Test_offline_PaperAndLiquid(object):
    @allure.title('离线试纸质控液')
    @pytest.mark.run(order=1)
    @pytest.mark.dependency(name='upload')
    def test_offline_PaperAndLiquid(self):
        logger.getlogger().info('测试的接口:%s', url.format('offline/qc/getPaperAndLiquid'))
        print("---------离线试纸质控液查询----------")
        sql1 = """delete from paper """
        sql2 = """delete from liquid """
        sqlite().delete(sql1)
        sqlite().delete(sql2)
        info = requests.post(url.format('offline/qc/getPaperAndLiquid'), headers=offilne.headers, data=
        json.dumps({})).json()
        print(info)
        logger.getlogger().debug('试纸质控液查询：传参%s返回体%s', {}, info)
        for i in info['data']['paperList']:
            sql = """INSERT INTO "paper"("id", "batchNum", "specs", "paperNum", "productionDate", "expiryDate", "lowMaxLimit", "lowMinLimit",
                    "mediumMaxLimit", "mediumMinLimit", "highMaxLimit", "highMinLimit", "createTime", "enterName")
            VALUES(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\',
                   \'{}\', \'{}\')""".format(i['id'], i['batchNum'], i['specs'], i['paperNum'], i['productionDate'],
                                             i['expiryDate'],
                                             i['lowMaxLimit'], i['lowMinLimit'], i['mediumMaxLimit'],
                                             i['mediumMinLimit'], i['highMaxLimit'],
                                             i['highMinLimit'], i['createTime'], i['enterName'])
            sqlite().insert(sql)
        sql = 'select count(*) from paper'
        assert len(info['data']['paperList']) == sqlite().select_id(sql)[0][0]

        for j in info['data']['liquidList']:
            sql = """INSERT INTO "main"."liquid"("id", "specs", "batchNum", "liquidNum", "type", "productionDate", "expiryDate", "createTime", "enterName") 
            VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')""".format(j['id'],
                                                                                                      j['specs'],
                                                                                                      j['batchNum'],
                                                                                                      j['liquidNum'],
                                                                                                      j['type'],
                                                                                                      j['productionDate'],
                                                                                                      j['expiryDate'],
                                                                                                      j['createTime'],
                                                                                                      j['enterName'])
            sqlite().insert(sql)
        sql = 'select count(*) from liquid'
        assert len(info['data']['liquidList']) == sqlite().select_id(sql)[0][0]

