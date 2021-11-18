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


@allure.feature("离线科室")
class Test_offline_dept(object):
    @allure.title('离线科室列表')
    @pytest.mark.run(order=1)
    @pytest.mark.dependency(name='upload')
    def test_offline_dept(self):
        logger.getlogger().info('测试的接口:%s', url.format('offline/common/dept/list'))
        print("---------离线科室查询----------")
        sql = """delete from dept """
        sqlite().delete(sql)
        info = requests.post(url.format('offline/common/dept/list'), headers=offilne.headers, data=
        json.dumps({})).json()
        logger.getlogger().debug('科室列表查询：传参%s返回体%s', {}, info)

        for i in info['data']:
            sql = """INSERT INTO "dept"("id", "name")
            VALUES(\'{}\', \'{}\')""".format(i['id'], i['name']
                                          )
            sqlite().insert(sql)
        sql ="select count(*) from dept"

        assert sqlite().select_id(sql)[0][0] == len(info['data'])

