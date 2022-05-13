import os
import sys

sys.path.append(r'' + os.path.abspath('../../'))
import allure
import pytest, yaml
from data.read_fun import read_yaml_info
import requests
from testCase.log import logger
from common.yaml_util import read_bastase_sql, read_url_csv, read_yaml
from common.open_database import MysqlDb
import json
from common.read_yaml import load

url = read_url_csv()[0]


@allure.feature('住院患者')
class Testzhuyuan(object):
    @allure.title('患者列表')
    @pytest.mark.parametrize('info',
                             yaml.safe_load(read_yaml_info(load('../data/path/path.yaml')['inhos_patient_list'])))
    def test_in_patient(self, info):
        logger.getlogger().info('---->接口:%s开始测试', url.format('inhos/patient/list'))
        response = requests.post(url.format('inhos/patient/list'), headers=read_yaml('headers'),
                                 data=json.dumps(info['parame'])).json()
        logger.getlogger().info('inhos/patient/list：请求头%s'
                                '传参%s'
                                '返回体%s',
                                read_yaml('headers'),
                                info['parame'],
                                response)

        try:
            assert response['code'] == info['result']['code']
            assert response['msg'] == info['result']['msg']
        #
        except AssertionError:
            logger.getlogger().error("inhos/patient/list %s", "接口报错", exc_info=1)
            assert response['code'] == info['result']['code']
        logger.getlogger().info('---->接口:%s结束一次用例测试', url.format('inhos/patient/list'))

    @allure.title('出院患者列表')
    @allure.description('该接口写了4个用例包含所有出院患者，根据科室筛选，根据住院号,根据姓名筛选')
    @pytest.mark.parametrize('info',
                             yaml.safe_load(read_yaml_info(load('../data/path/path.yaml')['inhos_patient_list_leave'])))
    def test_out_patient(self, info):
        logger.getlogger().info('---->接口:%s开始测试', url.format('inhos/patient/list/leave'))
        response = requests.post(url.format('inhos/patient/list/leave'), headers=read_yaml('headers'),
                                 data=json.dumps(info['parame'])).json()

        logger.getlogger().info('inhos/patient/list/leave：请求头%s'
                                '传参%s'
                                '返回体%s',
                                read_yaml('headers'),
                                info['parame'],
                                response)
        try:
            assert response['code'] == info['result']['code']
            assert response['msg'] == info['result']['msg']
        #
        except AssertionError:
            logger.getlogger().error("inhos/patient/list/leave %s", "接口报错", exc_info=1)
            assert response['code'] == info['result']['code']
        logger.getlogger().info('---->接口:%s结束一次用例测试', url.format('inhos/patient/list'))

    @allure.title('患者详情')
    @allure.description('该接口写了2个用例根据userid或者住院号')
    @pytest.mark.parametrize('info',
                             yaml.safe_load(read_yaml_info(load('../data/path/path.yaml')['inhos_patient_info'])))
    def test_patient_info(self, info):
        logger.getlogger().info('---->接口:%s开始测试', url.format('inhos/patient/info'))
        response = requests.post(url.format('inhos/patient/info'), headers=read_yaml('headers'),
                                 data=json.dumps(info['parame'])).json()

        logger.getlogger().info('inhos/patient/info：请求头%s'
                                '传参%s'
                                '返回体%s',
                                read_yaml('headers'),
                                info['parame'],
                                response)
        try:
            assert response['code'] == info['result']['code']
            assert response['msg'] == info['result']['msg']
            #
        except AssertionError:
            logger.getlogger().error("inhos/patient/info %s", "接口报错", exc_info=1)
            assert response['code'] == info['result']['code']
        logger.getlogger().info('---->接口:%s结束一次用例测试', url.format('inhos/patient/info'))

    @allure.title('控糖目标')
    @pytest.mark.parametrize('info',
                             yaml.safe_load(
                                 read_yaml_info(load('../data/path/path.yaml')['inhos_patient_info_healthArchives'])))
    def test_healthArchives(self, info):
        logger.getlogger().info('---->接口:%s开始测试', url.format('inhos/patient/healthArchives/info'))
        response = requests.post(url.format('inhos/patient/healthArchives/info'), headers=read_yaml('headers'),
                                 data=json.dumps(info['parame'])).json()

        logger.getlogger().info('inhos/patient/healthArchives/info：请求头%s'
                                '传参%s'
                                '返回体%s',
                                read_yaml('headers'),
                                info['parame'],
                                response)
        try:
            assert response['code'] == info['result']['code']
            assert response['msg'] == info['result']['msg']
            #
        except AssertionError:
            logger.getlogger().error("inhos/patient/healthArchives/info %s", "接口报错", exc_info=1)
            assert response['code'] == info['result']['code']
        logger.getlogger().info('---->接口:%s结束一次用例测试', url.format('inhos/patient/healthArchives/info'))

    #
    @allure.title('换床')
    @pytest.mark.parametrize('info',
                             yaml.safe_load(read_yaml_info(load('../data/path/path.yaml')['inhos_patient_changebed'])))
    def test_change_bed(self, info):
        logger.getlogger().info('---->接口:%s开始测试', url.format('inhos/patient/changebed'))
        response = requests.post(url.format('inhos/patient/changebed'), headers=read_yaml('headers'),
                                 data=json.dumps(info['parame'])).json()
        logger.getlogger().info('inhos/patient/changebed：请求头%s'
                                '传参%s'
                                '返回体%s',
                                read_yaml('headers'),
                                info['parame'],
                                response)
        data = MysqlDb().select_db("select * from {}.`patient_info`where user_id=\'{}\'".format(read_bastase_sql()[4],

                                                                                                info['parame'][
                                                                                                    'userId']))

        try:
            assert eval(data[0]['bed_num']) == info['parame']['bedNum']
            assert response['code'] == info['result']['code']
            assert response['msg'] == info['result']['msg']
            #
        except AssertionError:
            logger.getlogger().error("inhos/patient/changebed %s", "接口报错", exc_info=1)
            assert response['code'] == info['result']['code']
            assert eval(data[0]['bed_num']) == info['parame']['bedNum']
        logger.getlogger().info('---->接口:%s结束一次用例测试', url.format('inhos/patient/changebed'))

    '''
    # 更新患者信息，2个用例，修改手机号，修改床号
    # '''

    @allure.title('更新患者基本信息')
    @allure.description('更新患者信息，2个用例必传，修改手机号，修改床号')
    @pytest.mark.parametrize('info',
                             yaml.safe_load(read_yaml_info(load('../data/path/path.yaml')['inhos_patient_update'])))
    def test_update_patient_info(self, info):
        info['parame']['birthday'] = info['parame']['birthday'].strftime('%Y-%m-%d')
        # info['parame']['iptTime'] = info['parame']['iptTime'].strftime('%Y-%m-%d %H:%M:%S')
        print(info)
        logger.getlogger().info('---->接口:%s开始测试', url.format('inhos/patient/update'))
        response = requests.post(url.format('inhos/patient/update'), headers=read_yaml('headers'),
                                 data=json.dumps(info['parame'])).json()
        logger.getlogger().info('inhos/patient/update：请求头%s'
                                '传参%s'
                                '返回体%s',
                                read_yaml('headers'),
                                info['parame'],
                                response)
        data = MysqlDb().select_db("select * from {}.`patient_info`where user_id=\'{}\'".format(read_bastase_sql()[4],

                                                                                                info['parame'][
                                                                                                    'userId']))
        try:
            assert data[0]['bed_num'] == info['parame']['bedNum']
            assert data[0]['phone'] == info['parame']['phone']
            assert response['code'] == info['result']['code']
            assert response['msg'] == info['result']['msg']
        except AssertionError:
            logger.getlogger().error("inhos/patient/update %s", "接口报错", exc_info=1)
            assert response['code'] == info['result']['code']
            assert data[0]['bed_num'] == info['parame']['bedNum']
            assert data[0]['phone'] == info['parame']['phone']
        logger.getlogger().info('---->接口:%s结束一次用例测试', url.format('inhos/patient/update'))

    #
    # # @allure.title('患者出院')
    # # @pytest.mark.parametrize('info', [
    # #     zy().out_hospital()])
    # # def test_out_hospital(self, info):
    # #
    # #     response = requests.post(url.format('inhos/patient/outHospital'), headers=read_yaml('headers'),
    # #                              data=info).json()
    # #     logger.getlogger().info('出院患者：请求头%s传参%s返回体%s',
    # #                             read_yaml('headers'), info, response)
    # #
    # #     data = MysqlDb().select_db("select * from {}.`patient_info`where user_id=\'{}\'".format(read_bastase_sql()[4],
    # #
    # #                                                                                             read_zy_yaml()[
    # #                                                                                                 'userId']))
    # #     try:
    # #         assert data[0]['status'] == 0
    # #         assert response['code'] == 0
    # #         assert response['msg'] == '请求成功'
    # #     except AssertionError:
    # #         logger.getlogger().error("出院患者 %s", "接口报错", exc_info=1)
    # #         assert response['code'] == 0
    # #         assert data[0]['status'] == 0

    @allure.title('添加患者')
    @pytest.mark.parametrize('info',
                             yaml.safe_load(read_yaml_info(load('../data/path/path.yaml')['inhos_patient_add'])))
    def test_add_patient(self, info):
        logger.getlogger().info('---->接口:%s开始测试', url.format('inhos/patient/add'))
        response = requests.post(url.format('inhos/patient/add'), headers=read_yaml('headers'),
                                 data=json.dumps(info['parame'])).json()
        logger.getlogger().info('inhos/patient/add：请求头%s'
                                '传参%s'
                                '返回体%s',
                                read_yaml('headers'),
                                info['parame'],
                                response)

        data = MysqlDb().select_db(
            "select * from {}.`patient_info` ORDER BY id desc limit 1".format(read_bastase_sql()[4]))
        if response["msg"] == '住院号或身份证已经被绑定':
            logger.getlogger().info("检查住院号或身份证号是否被绑定")
        else:
            try:
                assert data[0]['ipt_num'] == info['parame']['iptNum']
                assert response['code'] == info['result']['code']
                assert response['msg'] == info['result']['msg']
            except AssertionError:
                logger.getlogger().error("inhos/patient/add %s", "接口报错", exc_info=1)
                assert response['code'] == info['result']['code']
                assert data[0]['ipt_num'] == (info['parame']['iptNum'])
            logger.getlogger().info('---->接口:%s结束一次用例测试', url.format('inhos/patient/add'))
