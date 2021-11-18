# coding=UTF-8
import os
import sys

sys.path.append(r'' + os.path.abspath('../../'))
import allure
import pytest
import requests
from testCase.basc import configHttp
from testCase.log import logger

url = "http://47.111.0.135:11145/vivachekcloud/api/{}"


@allure.feature('在线接口')
class Testlogin(object):
    @pytest.fixture()
    def login(self):
        response = requests.post(url.format('login'), headers=configHttp.getheader(), data=configHttp.login())
        headers = configHttp.getheader()
        headers["Access-Token"] = response.json()['data']['accessToken']
        headers["refresh_token"] = response.json()['data']['refreshToken']

        return headers

    @allure.story('登陆接口')
    def test_login(self):
        response = requests.post(url.format('login'), headers=configHttp.getheader(),
                                 data=configHttp.login()).json()
        logger.getlogger().debug('登陆接口：传参%s返回体%s', configHttp.login(), response['data'])
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
            print(response)
        except AssertionError:
            logger.getlogger().error("登陆后台 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('住院患者')
    def test_in_patient(self, login):
        head = login
        response = requests.post(url.format('inhos/patient/list'), headers=head, data=configHttp.in_patient()).json()
        logger.getlogger().debug('住院患者信息：%s%s', configHttp.in_patient(), response['data'])
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
            print(response)
            configHttp.get_userid(response['data']['lists'][0]['userId'],
                                  response['data']['lists'][1]['userId'],
                                  response['data']['lists'][0]['iptNum'],
                                  response['data']['lists'][0]['name'],
                                  response['data']['lists'][0]['deptId'],
                                  response['data']['lists'][0]['deptName']
                                  )
        except AssertionError:
            logger.getlogger().error("住院患者后台 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('患者统计')
    def test_patient_count(self, login):
        head = login
        response = requests.post(url.format('inhos/measure/count/patient'), headers=head,
                                 data=configHttp.patient_count()).json()
        logger.getlogger().debug('患者统计的信息：传参%s返回体%s', configHttp.patient_count(), response['data'])
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("患者统计 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('添加患者')
    def test_add_patient(self, login):
        head = login
        response = requests.post(url.format('inhos/patient/add'), headers=head,
                                 data=configHttp.add_patient()).json()
        logger.getlogger().debug('添加患者的信息：传参%s返回体%s', configHttp.add_patient(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("添加患者 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('出院患者')
    def test_out_patient(self, login):
        head = login
        response = requests.post(url.format('inhos/patient/list/leave'), headers=head,
                                 data=configHttp.out_patient()).json()
        logger.getlogger().debug('出院患者信息：传参%s返回体%s', configHttp.out_patient(), response['data'])
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("出院患者 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('获取控糖目标')
    def test_healthArchives(self, login):
        head = login
        response = requests.post(url.format('inhos/patient/healthArchives/info'), headers=head,
                                 data=configHttp.healthArchives()).json()
        logger.getlogger().debug('控糖目标信息：传参%s返回体%s', configHttp.healthArchives(), response['data'])
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("控糖目标 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('获取患者基本信息')
    def test_patient_info(self, login):
        head = login
        response = requests.post(url.format('inhos/patient/info'), headers=head,
                                 data=configHttp.patient_info()).json()
        logger.getlogger().debug('患者基本信息：传参%s返回体%s', configHttp.patient_info(), response['data'])
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("获取患者基本 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('更新患者基本信息')
    def test_update_patient_info(self, login):
        head = login
        response = requests.post(url.format('inhos/patient/update'), headers=head,
                                 data=configHttp.update_patient_info()).json()
        logger.getlogger().debug('更新患者的信息：传参%s返回体%s', configHttp.update_patient_info(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("更新患者信息 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('换床')
    def test_change_bed(self, login):
        head = login
        response = requests.post(url.format('inhos/patient/changebed'), headers=head,
                                 data=configHttp.change_bed()).json()
        logger.getlogger().debug('换床的信息：传参%s返回体%s', configHttp.change_bed(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("换床 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    # @allure.story('转科')
    # def test_change_dept(self, login):
    #     head = login
    #     response = requests.post(url.csv.format('inhos/patient/transfer'), headers=head,
    #                              data=configHttp.change_dept()).json()
    #     logger.getlogger().debug('转科的信息：传参%s返回体%s', configHttp.change_dept(), response)
    #     try:
    #         assert response['code'] == 0
    #         assert response['msg'] == '请求成功'
    #     except AssertionError:
    #         logger.getlogger().error("转科 %s", "接口报错", exc_info=1)
    #         assert response['code'] == 0

    # @allure.story('出院')
    # def test_out_hospital(self, login):
    #     head = login
    #     response = requests.post(url.csv.format('inhos/patient/outHospital'), headers=head,
    #                              data=configHttp.out_hospital()).json()
    #     logger.getlogger().debug('返回的信息：%s', response)
    #     try:
    #         assert response['code'] == 0
    #         assert response['msg'] == '请求成功'
    #     except AssertionError:
    #         logger.getlogger().error("后台 %s", "接口报错", exc_info=1)
    #         assert response['code'] == 0

    @allure.story('添加血糖')
    def test_add_glu(self, login):
        head = login
        response = requests.post(url.format('inhos/glu/add'), headers=head,
                                 data=configHttp.add_glu()).json()
        logger.getlogger().debug('添加血糖信息：传参%s返回体%s', configHttp.add_glu(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("添加血糖 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('患者血糖列表')
    def test_patient_glu_list(self, login):
        head = login
        response = requests.post(url.format('inhos/glu/list'), headers=head,
                                 data=configHttp.patient_glu_list()).json()
        logger.getlogger().debug('患者列表信息：传参%s返回体%s', configHttp.patient_glu_list(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
            configHttp.get_glu_id(response['data']['lists'][0]['id'])
        except AssertionError:
            logger.getlogger().error("患者列表 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('患者血糖报告')
    def test_patient_glu_report(self, login):
        head = login
        response = requests.post(url.format('inhos/glu/report'), headers=head,
                                 data=configHttp.patient_glu_report()).json()
        logger.getlogger().debug('血糖报告信息：传参%s返回体%s', configHttp.patient_glu_report(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("血糖报告 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('修改血糖')
    def test_update_glu(self, login):
        head = login
        response = requests.post(url.format('inhos/glu/update'), headers=head,
                                 data=configHttp.update_glu()).json()
        logger.getlogger().debug('修改血糖信息：传参%s返回体%s', configHttp.update_glu(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("修改血糖 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('获取血糖详情')
    def test_glu_info(self, login):
        head = login
        response = requests.post(url.format('inhos/glu/info'), headers=head,
                                 data=configHttp.glu_info()).json()
        logger.getlogger().debug('获取血糖详情的信息：传参%s返回体%s', configHttp.glu_info(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("获取血糖详情 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('患者血糖趋势图')
    def test_patientTrendChart(self, login):
        head = login
        response = requests.post(url.format('inhos/glu/patientTrendChart'), headers=head,
                                 data=configHttp.patientTrendChart()).json()
        logger.getlogger().debug('患者血糖趋势信息：传参%s返回体%s', configHttp.patientTrendChart(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("患者血糖趋势 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('患者血糖统计图')
    def test_patientPieChart(self, login):
        head = login
        response = requests.post(url.format('inhos/glu/patientPieChart'), headers=head,
                                 data=configHttp.patientPieChart()).json()
        logger.getlogger().debug('患者血糖统计图信息：传参%s返回体%s', configHttp.patientPieChart(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("患者血糖统计图 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    # @allure.story('删除血糖')
    # def test_del_glu(self, login):
    #     head = login
    #     response = requests.post(url.csv.format('inhos/glu/delete'), headers=head,
    #                              data=configHttp.del_glu()).json()
    #     logger.getlogger().debug('删除血糖信息：%s', response)
    #     try:
    #         assert response['code'] == 0
    #         assert response['msg'] == '请求成功'
    #     except AssertionError:
    #         logger.getlogger().error("删除血糖 %s", "接口报错", exc_info=1)
    #         assert response['code'] == 0

    @allure.story('血糖预警列表')
    def test_glu_alarmList(self, login):
        head = login
        response = requests.post(url.format('inhos/glu/alarmList'), headers=head,
                                 data=configHttp.glu_alarmList()).json()
        logger.getlogger().debug('血糖预警列表信息：传参%s返回体%s', configHttp.glu_alarmList(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
            configHttp.get_warn_info(response['data']['lists'][0]['id'])
        except AssertionError:
            logger.getlogger().error("血糖预警列表 传参%s返回体%s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('血糖预警处理')
    def test_glu_warning_update(self, login):
        head = login
        response = requests.post(url.format('inhos/glu/warning/update'), headers=head,
                                 data=configHttp.glu_warning_update()).json()
        logger.getlogger().debug('血糖预警处理信息：传参%s返回体%s', configHttp.glu_warning_update(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("血糖预警处理 传参%s返回体%s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('添加任务')
    def test_add_glu_order(self, login):
        head = login
        response = requests.post(url.format('inhos/measure/glu_order/add'), headers=head,
                                 data=configHttp.add_glu_order()).json()
        logger.getlogger().debug('添加任务信息：传参%s返回体%s', configHttp.add_glu_order(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("添加任务 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('患者任务列表')
    def test_glu_order_getPatientOrderList(self, login):
        head = login
        response = requests.post(url.format('inhos/measure/glu_order/getPatientOrderList'), headers=head,
                                 data=configHttp.glu_order_getPatientOrderList()).json()
        logger.getlogger().debug('患者任务列表信息：传参%s返回体%s', configHttp.glu_order_getPatientOrderList(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
            configHttp.get_order_id(response['data']['list'][0]['id'])
        except AssertionError:
            logger.getlogger().error("患者任务列表 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('任务详情')
    def test_glu_order_info(self, login):
        head = login
        response = requests.post(url.format('inhos/measure/glu_order/info'), headers=head,
                                 data=configHttp.glu_order_info()).json()
        logger.getlogger().debug('任务详情信息：传参%s返回体%s', configHttp.glu_order_info(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("任务详情 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('编辑任务')
    def test_update_glu_order(self, login):
        head = login
        response = requests.post(url.format('inhos/measure/glu_order/update'), headers=head,
                                 data=configHttp.update_glu_order()).json()
        logger.getlogger().debug('编辑任务信息：传参%s返回体%s', configHttp.update_glu_order(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("编辑任务 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('停止任务')
    def test_stop_glu_info(self, login):
        head = login
        response = requests.post(url.format('inhos/measure/glu_order/stop'), headers=head,
                                 data=configHttp.stop_glu_info()).json()
        logger.getlogger().debug('停止任务信息：传参%s返回体%s', configHttp.stop_glu_info(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("停止任务 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    # @allure.story('app停止今日任务')
    # def test_glu_order_monitorListr(self, login):
    #     head = login
    #     response = requests.post(url.csv.format('inhos/measure/glu_order/stopMeasure'), headers=head,
    #                              data=configHttp.glu_order_monitorList()).json()
    #     logger.getlogger().debug('返回的信息：%s', response)
    #     try:
    #         assert response['code'] == 0
    #         assert response['msg'] == '请求成功'
    #     except AssertionError:
    #         logger.getlogger().error("后台 %s", "接口报错", exc_info=1)
    #         assert response['code'] == 0

    # @allure.story('任务添加血糖 app')
    # def test_glu_order_addMeasure(self, login):
    #     head = login
    #     response = requests.post(url.csv.format('inhos/measure/glu_order/addMeasure'), headers=head,
    #                              data=configHttp.glu_order_addMeasure()).json()
    #     logger.getlogger().debug('返回的信息：%s', response)
    #     try:
    #         assert response['code'] == 0
    #         assert response['msg'] == '请求成功'
    #     except AssertionError:
    #         logger.getlogger().error("后台 %s", "接口报错", exc_info=1)
    #         assert response['code'] == 0

    @allure.story('检测任务列表')
    def test_glu_order_web_monitorList(self, login):
        head = login
        response = requests.post(url.format('inhos/measure/glu_order/web_monitorList'), headers=head,
                                 data=configHttp.glu_order_web_monitorList()).json()
        logger.getlogger().debug('检测任务列表信息：传参%s返回体%s', configHttp.glu_order_web_monitorList(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("检测任务列表 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    # @allure.story('app院内检测')
    # def test_glu_app_measureGluList(self, login):
    #     head = login
    #     response = requests.post(url.csv.format('inhos/measure/glu_order/web_monitorList'), headers=head,
    #                              data=configHttp.glu_app_measureGluList()).json()
    #     logger.getlogger().debug('返回的信息：%s', response)
    #     try:
    #         assert response['code'] == 0
    #         assert response['msg'] == '请求成功'
    #     except AssertionError:
    #         logger.getlogger().error("后台 %s", "接口报错", exc_info=1)
    #         assert response['code'] == 0
    @allure.story('添加临时检测')
    def test_measure_temp_add(self, login):
        head = login
        response = requests.post(url.format('inhos/measure/temp/add'), headers=head,
                                 data=configHttp.measure_temp_add()).json()
        logger.getlogger().debug('添加临时检测信息：传参%s返回体%s', configHttp.measure_temp_add(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("添加临时检测 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('临时检测列表')
    def test_measure_temp_list(self, login):
        head = login
        response = requests.post(url.format('inhos/measure/temp/list'), headers=head,
                                 data=configHttp.measure_temp_list()).json()
        logger.getlogger().debug('临时检测列表信息：传参%s返回体%s', configHttp.measure_temp_list(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
            configHttp.get_ls_id(response['data']['lists'][0]['id'])
        except AssertionError:
            logger.getlogger().error("临时检测列表 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('临时检测血糖详情')
    def test_measure_temp_info(self, login):
        head = login
        response = requests.post(url.format('inhos/measure/temp/info'), headers=head,
                                 data=configHttp.measure_temp_info()).json()
        logger.getlogger().debug('临时检测血糖详情信息：传参%s返回体%s', configHttp.measure_temp_info(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("临时检测血糖详情 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('编辑临时检测血糖')
    def test_measure_temp_update(self, login):
        head = login
        response = requests.post(url.format('inhos/measure/temp/update'), headers=head,
                                 data=configHttp.measure_temp_update()).json()
        logger.getlogger().debug('编辑临时检测血糖信息：传参%s返回体%s', configHttp.measure_temp_update(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("编辑临时检测血糖 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    # @allure.story('删除临时检测血糖')
    # def test_measure_temp_delete(self, login):
    #     head = login
    #     response = requests.post(url.csv.format('inhos/measure/temp/delete'), headers=head,
    #                              data=configHttp.measure_temp_delete()).json()
    #     logger.getlogger().debug('删除临时检测血糖信息：%s', response)
    #     try:
    #         assert response['code'] == 0
    #         assert response['msg'] == '请求成功'
    #     except AssertionError:
    #         logger.getlogger().error("删除临时检测血糖 %s", "接口报错", exc_info=1)
    #         assert response['code'] == 0

    @allure.story('上传离线临时检测血糖')
    def test_measure_temp_uploadMeasures(self, login):
        head = login
        response = requests.post(url.format('inhos/measure/temp/uploadMeasures'), headers=head,
                                 data=configHttp.measure_temp_uploadMeasures()).json()
        logger.getlogger().debug('上传离线临时检测血糖信息：传参%s返回体%s', configHttp.measure_temp_uploadMeasures(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("上传离线临时检测血糖 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    # @allure.story('添加设备')
    # def test_device_add(self, login):
    #     head = login
    #     response = requests.post(url.csv.format('device/add/single'), headers=head,
    #                              data=configHttp.device_add()).json()
    #     logger.getlogger().debug('返回的信息：%s', response)
    #     try:
    #         assert response['code'] == 0
    #         assert response['msg'] == '请求成功'
    #     except AssertionError:
    #         logger.getlogger().error("后台 %s", "接口报错", exc_info=1)
    #         assert response['code'] == 0
    @allure.story('添加试纸')
    def test_paper_add(self, login):
        head = login
        response = requests.post(url.format('paper/add/single'), headers=head,
                                 data=configHttp.paper_add()).json()
        logger.getlogger().debug('添加试纸信息：传参%s返回体%s', configHttp.paper_add(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("添加试纸 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('查询试纸')
    def test_paper_info(self, login):
        head = login
        response = requests.post(url.format('paper/list'), headers=head,
                                 data=configHttp.paper_info()).json()
        logger.getlogger().debug('查询试纸信息：传参%s返回体%s', configHttp.paper_info(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
            configHttp.get_paper(response['data']['lists'][0]['id'])
        except AssertionError:
            logger.getlogger().error("查询试纸 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('编辑试纸')
    def test_paper_update(self, login):
        head = login
        response = requests.post(url.format('paper/update'), headers=head,
                                 data=configHttp.paper_update()).json()
        logger.getlogger().debug('编辑试纸信息：传参%s返回体%s', configHttp.paper_update(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("编辑试纸 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('删除试纸')
    def test_paper_del(self, login):
        head = login
        response = requests.post(url.format('paper/delete'), headers=head,
                                 data=configHttp.paper_del()).json()
        logger.getlogger().debug('删除试纸信息：传参%s返回体%s', configHttp.paper_del(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("删除试纸 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('添加质控液')
    def test_liquid_add(self, login):
        head = login
        response = requests.post(url.format('qc/liquid/add/single'), headers=head,
                                 data=configHttp.liquid_add()).json()
        logger.getlogger().debug('添加质控液信息：传参%s返回体%s', configHttp.liquid_add(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("添加质控液 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('查询质控液')
    def test_liquid_info(self, login):
        head = login
        response = requests.post(url.format('qc/liquid/list'), headers=head,
                                 data=configHttp.liquid_info()).json()
        logger.getlogger().debug('查询质控液信息：传参%s返回体%s', configHttp.liquid_info(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
            configHttp.get_liquid(response['data']['lists'][0]['id'])
        except AssertionError:
            logger.getlogger().error("查询质控液 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('编辑质控液')
    def test_liquid_update(self, login):
        head = login
        response = requests.post(url.format('qc/liquid/update'), headers=head,
                                 data=configHttp.liquid_update()).json()
        logger.getlogger().debug('编辑质控液信息：传参%s返回体%s', configHttp.liquid_update(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("编辑质控液 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('删除质控液')
    def test_liquid_del(self, login):
        head = login
        response = requests.post(url.format('qc/liquid/delete'), headers=head,
                                 data=configHttp.liquid_del()).json()
        logger.getlogger().debug('返回的信息：传参%s返回体%s', configHttp.liquid_del(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("后台 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('质控列表')
    def test_qc_record_list(self, login):
        head = login
        response = requests.post(url.format('qc/record/list'), headers=head, data=configHttp.qc_record_list()).json()
        logger.getlogger().debug('质控列表信息：传参%s返回体%s', configHttp.qc_record_list(), response['data'])
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("质控列表 %s", "接口报错", exc_info=1)

    @allure.story('添加质控')
    def test_qc_record_add(self, login):
        head = login
        response = requests.post(url.format('qc/record/add'), headers=head,
                                 data=configHttp.qc_record_add()).json()
        logger.getlogger().debug('添加质控信息：传参%s返回体%s', configHttp.qc_record_add(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("添加质控 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('编辑质控')
    def test_qc_record_update(self, login):
        head = login
        response = requests.post(url.format('qc/record/update'), headers=head,
                                 data=configHttp.qc_record_update()).json()
        logger.getlogger().debug('编辑质控的信息：传参%s返回体%s', configHttp.qc_record_update(), response)

        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("编辑质控 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('删除质控')
    def test_qc_record_del(self, login):
        head = login
        response = requests.post(url.format('qc/record/delete'), headers=head,
                                 data=configHttp.qc_record_del()).json()
        logger.getlogger().debug('删除质控的信息：传参%s返回体%s', configHttp.qc_record_del(), response)

        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("删除质控 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('质控分析列表')
    def test_qc_record_analysis(self, login):
        head = login
        response = requests.post(url.format('qc/record/analysis'), headers=head,
                                 data=configHttp.qc_record_analysis()).json()
        logger.getlogger().debug('质控分析列表的信息：传参%s返回体%s', configHttp.qc_record_analysis(), response)

        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("质控分析列表 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('质控统计列表')
    def test_qc_record_statistics(self, login):
        head = login
        response = requests.post(url.format('qc/record/statistics'), headers=head,
                                 data=configHttp.qc_record_statistics()).json()
        logger.getlogger().debug('质控统计列表：传参%s返回体%s', configHttp.qc_record_statistics(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("质控统计列表 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    # @allure.story('导出质控统计列表')
    # def test_qc_export(self, login):
    #     head = login
    #     Platform = head['Platform']
    #     Version = head['Version']
    #     Project = head['Project']
    #     Access_Token = head["Access-Token"]
    #     print(url.csv.format('qc/record/list/export') + '?' +
    #           'Platform=' + Platform + '&' +
    #           'Version=' + Version + '&' +
    #           'Project=' + Project + '&' +
    #           'Access-Token=' + Access_Token)
    #
    #     response = requests.get(url.csv.format('qc/record/list/export') + '?' +
    #                             'Platform=' + Platform + '&' +
    #                             'Version=' + Version + '&' +
    #                             'Project=' + Project + '&' +
    #                             'Access-Token=' + Access_Token).json()
    #     print(response)
    #     logger.getlogger().debug('导出质控统计列表信息：%s', response)
    #     try:
    #         assert response['code'] == 0
    #         assert response['msg'] == '请求成功'
    #     except AssertionError:
    #         logger.getlogger().error("导出质控统计列表 %s", "接口报错", exc_info=1)
    #         assert response['code'] == 0

    @allure.story('对比管理列表')
    def test_cp_manage_list(self, login):
        head = login
        response = requests.post(url.format('cp/manage/list'), headers=head,
                                 data=configHttp.cp_manage_list()).json()
        logger.getlogger().debug('对比管理列表的信息：传参%s返回体%s', configHttp.cp_manage_list(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("对比管理列表 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('web室间质评列表')
    def test_qc_record_external_list(self, login):
        head = login
        response = requests.post(url.format('qc/record/external/list'), headers=head,
                                 data=configHttp.qc_record_external_list()).json()
        logger.getlogger().debug('web室间质评列表信息：传参%s返回体%s', configHttp.qc_record_external_list(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
            configHttp.get_qc_record(response['data']['lists'][0]['id'],
                                     response['data']['lists'][0]['batchNum'],
                                     response['data']['lists'][0]['sampleNum'],
                                     response['data']['lists'][0]['sn']
                                     )
        except AssertionError:
            logger.getlogger().error("web室间质评列表 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('添加室间质评')
    def test_qc_record_external_add(self, login):
        head = login
        response = requests.post(url.format('qc/record/external/add'), headers=head,
                                 data=configHttp.qc_record_external_add()).json()
        logger.getlogger().debug('添加室间质评信息：传参%s返回体%s', configHttp.qc_record_external_add(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("添加室间质评 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('修改室间质评')
    def test_qc_record_external_update(self, login):
        head = login
        response = requests.post(url.format('qc/record/external/update'), headers=head,
                                 data=configHttp.qc_record_external_update()).json()
        logger.getlogger().debug('修改室间质评信息：传参%s返回体%s', configHttp.qc_record_external_update(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("修改室间质评 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    @allure.story('删除室间质评')
    def test_qc_record_external_del(self, login):
        head = login
        response = requests.post(url.format('qc/record/external/delete'), headers=head,
                                 data=configHttp.qc_record_external_del()).json()
        logger.getlogger().debug('删除室间质评信息：传参%s返回体%s', configHttp.qc_record_external_del(), response)
        try:
            assert response['code'] == 0
            assert response['msg'] == '请求成功'
        except AssertionError:
            logger.getlogger().error("删除室间质评 %s", "接口报错", exc_info=1)
            assert response['code'] == 0

    # @allure.story('导出室间质评列表')
    # def test_qc_external_export(self, login):
    #     head = login
    #     Platform = head['Platform']
    #     Version = head['Version']
    #     Project = head['Project']
    #     Access_Token = head["Access-Token"]
    #
    #     response = requests.get(url.csv.format('qc/record/external/export') + '?' +
    #                             "Platform=" + Platform + "&" +
    #                             "Version=" + Version + "&" +
    #                             "Project=" + Project + "&" +
    #                             "Access-Token=" + Access_Token + "&" +
    #                             "X-User-Agent=" + "web/chrome/91.0.4472.114").json()
    #     print(response)
    #     logger.getlogger().debug('导出室间质评列表：%s', response)
    #     try:
    #         assert response['code'] == 0
    #         assert response['msg'] == '请求成功'
    #     except AssertionError:
    #         logger.getlogger().error("导出室间质评列表后台 %s", "接口报错", exc_info=1)
    #         assert response['code'] == 0

    # @allure.story('退出接口')
    # def test_layout(self, login):
    #     head = login
    #     response = requests.post(url.csv.format('logout'), headers=head, data={}).json()
    #
    #     logger.getlogger().debug('返回的信息：%s', response)
    #     try:
    #         assert response['code'] == 0
    #         assert response['msg'] == '请求成功'
    #     except AssertionError:
    #         logger.getlogger().error("后台 %s", "接口报错", exc_info=1)
    #         assert response['code'] == 0


if __name__ == '__main__':
    pytest.main(["-s", 'test_log.py', '--alluredir', '../../result'])
    os.system(
        'allure generate ../../result -o ../../report_allure --clean')
