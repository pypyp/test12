import os
import sys

sys.path.append(r'' + os.path.abspath('../../'))
import allure
import pytest
import requests
from data.zy_patient import zy
from testCase.log import logger
from common.yaml_util import read_yaml, read_zy_yaml, read_bastase_sql, read_url_csv
from common.open_database import MysqlDb
import json

url = read_url_csv()[0]


@allure.feature('住院患者')
class Testzhuyuan(object):
    @allure.title('患者列表')
    @allure.description('该接口写了4个用例包含所有患者，根据科室筛选，根据床号筛选，根据住院号筛选')
    @pytest.mark.parametrize('info', [zy().in_patient_0(),
                                      zy().in_patient_1(),
                                      zy().in_patient_2(),
                                      zy().in_patient_3()])
    def test_in_patient(self, info):
        logger.getlogger().info('测试的接口:%s', url.format('mz/patient/list'))
        response = requests.post(url.format('mz/patient/list'), headers=read_yaml('headers'),
                                 data=info).json()
        logger.getlogger().info('住院患者：请求头%s传参%s返回体%s',
                                read_yaml('headers'), info, response)

        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'

        except AssertionError:
            logger.getlogger().error("住院患者 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.title('出院患者列表')
    @allure.description('该接口写了4个用例包含所有出院患者，根据科室筛选，根据住院号,根据姓名筛选')
    @pytest.mark.parametrize('info', [zy().out_patient_0(),
                                      zy().out_patient_1(),
                                      zy().out_patient_2(),
                                      zy().out_patient_3()])
    def test_out_patient(self,info):
        logger.getlogger().info('测试的接口:%s', url.format('inhos/patient/list/leave'))
        response = requests.post(url.format('inhos/patient/list/leave'), headers=read_yaml('headers'),
                                 data=info).json()

        logger.getlogger().info('出院患者：请求头%s传参%s返回体%s',
                                read_yaml('headers'), info, response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("出院患者 %s", "接口报错", exc_info=1)
            assert response['code'] == 0


    @allure.title('患者详情')
    @allure.description('该接口写了2个用例根据userid或者住院号')
    @pytest.mark.parametrize('info',[zy().patient_info_0(),
                                    zy().patient_info_1()])
    def test_patient_info(self, info):
        logger.getlogger().info('测试的接口:%s', url.format('inhos/patient/info'))
        response = requests.post(url.format('inhos/patient/info'), headers=read_yaml('headers'),
                                 data=info).json()

        logger.getlogger().info('患者详情：请求头%s传参%s返回体%s',
                                read_yaml('headers'), info, response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("患者详情 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.title('控糖目标')
    @pytest.mark.parametrize('info', [zy().healthArchives()])
    def test_healthArchives(self, info):
        logger.getlogger().info('测试的接口:%s', url.format('inhos/patient/healthArchives/info'))
        response = requests.post(url.format('inhos/patient/healthArchives/info'), headers=read_yaml('headers'),
                                 data=info).json()
        logger.getlogger().info('患者控糖目标：请求头%s传参%s返回体%s',
                                read_yaml('headers'), info, response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("患者控糖目标 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.title('换床')
    @pytest.mark.parametrize('info', [zy().change_bed0(),
                                      zy().change_bed1()])
    def test_change_bed(self, info):
        logger.getlogger().info('测试的接口:%s', url.format('inhos/patient/changebed'))
        response = requests.post(url.format('inhos/patient/changebed'), headers=read_yaml('headers'),
                                 data=info).json()
        logger.getlogger().info('换床：请求头%s传参%s返回体%s',
                                read_yaml('headers'), info, response)
        data = MysqlDb().select_db("select * from {}.`patient_info`where user_id=\'{}\'".format(read_bastase_sql()[4],

                                                                         read_zy_yaml()['userId'] ))
        print(data[0]['bed_num'],json.loads(info)['bedNum'])
        try:
            assert eval(data[0]['bed_num']) == eval(str(json.loads(info)['bedNum']))
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("换床 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
            assert eval(data[0]['bed_num']) == eval(str(json.loads(info)['bedNum']))

    '''
    更新患者信息，2个用例，修改手机号，修改床号
    '''
    @allure.title('更新患者基本信息')
    @allure.description('更新患者信息，2个用例必传，修改手机号，修改床号')
    @pytest.mark.parametrize('info',[
                                     zy().update_patient_info_1(),
                                     zy().update_patient_info_2()
    ])
    def test_update_patient_info(self,info):
        logger.getlogger().info('测试的接口:%s', url.format('inhos/patient/update'))
        response = requests.post(url.format('inhos/patient/update'), headers=read_yaml('headers'),
                                 data=info).json()
        logger.getlogger().info('更新患者：请求头%s传参%s返回体%s',
                                read_yaml('headers'), info, response)

        data = MysqlDb().select_db("select * from {}.`patient_info`where user_id=\'{}\'".format(read_bastase_sql()[4],

                                                                             read_zy_yaml()['userId'] ))

        try:

            assert eval(data[0]['bed_num']) == eval(str(json.loads(info)['bedNum']))
            assert data[0]['phone'] == json.loads(info)['phone']
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("更新患者信息 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
            assert eval(data[0]['bed_num']) == eval(str(json.loads(info)['bedNum']))
            assert data[0]['phone'] == json.loads(info)['phone']



    # @allure.title('患者出院')
    # @pytest.mark.parametrize('info', [
    #     zy().out_hospital()])
    # def test_out_hospital(self, info):
    #
    #     response = requests.post(url.format('inhos/patient/outHospital'), headers=read_yaml('headers'),
    #                              data=info).json()
    #     logger.getlogger().info('出院患者：请求头%s传参%s返回体%s',
    #                             read_yaml('headers'), info, response)
    #
    #     data = MysqlDb().select_db("select * from {}.`patient_info`where user_id=\'{}\'".format(read_bastase_sql()[4],
    #
    #                                                                                             read_zy_yaml()[
    #                                                                                                 'userId']))
    #     try:
    #         assert data[0]['status'] == 0
    #         assert response['code'] == 0
    #         assert response['msg'] == '请求成功'
    #     except AssertionError:
    #         logger.getlogger().error("出院患者 %s", "接口报错", exc_info=1)
    #         assert response['code'] == 0
    #         assert data[0]['status'] == 0

    # @allure.title('扫码')
    # @pytest.mark.parametrize('info',[zy().scan()])
    # def test_scan_info(self, info):
    #     print(info)
    #     if read_yaml('headers')['Platform'] =='1':
    #         response = requests.post(url.format('inhos/patient/info/scan'), headers=read_yaml('headers'),
    #                                  data=info).json()
    #         print(response)
    #         logger.getlogger().info('扫码：请求头%s传参%s返回体%s',
    #                                 read_yaml('headers'), info, response)
    #         try:
    #             assert response['code'] == 0
    #             assert response['msg'] == '请求成功'
    #         except AssertionError:
    #             logger.getlogger().error("扫码 %s", "接口报错", exc_info=1)
    #             assert response['code'] == 0
    #     else:logger.getlogger().info("并不是医护端可能是web端请检查请求头")

    @allure.title('添加患者')
    @pytest.mark.parametrize('info', [zy().add_patient()])
    def test_add_patient(self, info):
        logger.getlogger().info('测试的接口:%s', url.format('inhos/patient/add'))
        response = requests.post(url.format('inhos/patient/add'), headers=read_yaml('headers'),
                                 data=info).json()

        logger.getlogger().info('登记患者：请求头%s传参%s返回体%s',
                                read_yaml('headers'), info, response)

        data = MysqlDb().select_db("select * from {}.`patient_info` ORDER BY id desc limit 1".format(read_bastase_sql()[4]))
        try:
            assert eval(data[0]['ipt_num']) == eval(str(json.loads(info)['iptNum']))
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("登记患者 %s", "接口报错", exc_info=1)
            assert response['code'] == 0
            assert eval(data[0]['ipt_num']) == eval(str(json.loads(info)['iptNum']))
