import os
import sys

sys.path.append(r'' + os.path.abspath('../../'))
import allure
import pytest
import requests
from data.zy_alarmList import zy_alarmlist
from testCase.log import logger
from common.yaml_util import read_yaml, read_zy_yaml, read_bastase_sql, read_url_csv
from common.open_database import MysqlDb
import json
url = read_url_csv()[0]

response = requests.post(url.format('inhos/glu/alarmList'), headers=read_yaml('headers'),
                         data=zy_alarmlist().glu_alarmList1()).json()

d2 = {'id1': '', 'id2': ''}

for i in response['data']['lists']:
    if d2['id1'] == '':
        if i['warningStatus'] == 0:
            d2['id1'] = i['id']
        continue
    if d2['id2'] == '':
        if i['warningStatus'] == 0:
            d2['id2'] = i['id']
        break
print(d2)
@allure.feature('血糖预警')
class Testzhuyuan(object):
    @allure.title('预警列表')



    @allure.title('预警列表')
    @allure.description('该接口写了3个用例全部预警，高血糖，低血糖')
    @pytest.mark.parametrize('info', [zy_alarmlist().glu_alarmList1(),
                                      zy_alarmlist().glu_alarmList2(),
                                      zy_alarmlist().glu_alarmList3(),
                                      ])
    def test_glu_alarmList(self,info):
        logger.getlogger().info('测试的接口:%s', url.format('inhos/glu/alarmList'))
        response = requests.post(url.format('inhos/glu/alarmList'), headers=read_yaml('headers'),
                                 data=info).json()
        logger.getlogger().info('住院患者：请求头%s传参%s返回体%s',
                                read_yaml('headers'), info, response)


        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'

        except AssertionError:
            logger.getlogger().error("住院患者 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.title('预警忽略')
    def test_alarmList_ignore(self):
        logger.getlogger().info('测试的接口:%s', url.format('inhos/glu/warning/update'))
        response = requests.post(url.format('inhos/glu/warning/update'), headers=read_yaml('headers'),
                                 data= json.dumps({'id':d2['id1'], "warningStatus":2})).json()
        logger.getlogger().info('住院患者：请求头%s传参%s返回体%s',
                                read_yaml('headers'), json.dumps({'id':d2['id1'], "warningStatus":2}), response)
        data = MysqlDb().select_db(
            "select * from {}.`blood_glucose_record` where id=\'{}\'".format(
                read_bastase_sql()[4],
                d2['id1']))
        try:
            assert data[0]['warning_status'] == 2
            assert response['code'] == 0
            assert response['msg'] == '请求成功'


        except AssertionError:
            logger.getlogger().error("住院患者 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
            assert data[0]['warning_status'] == 2

    @allure.title('预警处理')
    def test_alarmList_deal(self):
        logger.getlogger().info('测试的接口:%s', url.format('inhos/glu/warning/update'))
        response = requests.post(url.format('inhos/glu/warning/update'), headers=read_yaml('headers'),
                                 data=json.dumps({'id':d2['id2'], "warningStatus":1})).json()
        logger.getlogger().info('住院患者：请求头%s传参%s返回体%s',
                                read_yaml('headers'), json.dumps({'id':d2['id2'], "warningStatus":1}), response)
        data = MysqlDb().select_db(
            "select * from {}.`blood_glucose_record` where id=\'{}\'".format(
                read_bastase_sql()[4],
                d2['id2']))

        try:
            assert data[0]['warning_status'] == 1
            assert response['code'] == 0
            assert response['msg'] == '请求成功'

        except AssertionError:
            logger.getlogger().error("住院患者 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
            assert data[0]['warning_status'] == 1