# coding=UTF-8
# coding=utf-8
__author__ = "Enoch"
# 这是一个app登录的测试

from appium import webdriver
#
import unittest
import time
import warnings


class TestloginTest(object):
    def setup_class(self):

        warnings.simplefilter("ignore", ResourceWarning)
        desired_caps = {
            'platformName': 'Android',
            'deviceName': '359B0000072',
            'platformVersion': '7.0',
            # 'appPackage': 'com.vivachek.nova.cn',
            'appPackage': 'com.vivachek.nova.tnineeightzeroone',
            # 'appActivity': 'com.vivachek.vivachekdoctor.splash.SplashActivity'
            'appActivity': 'com.vivachek.t9801.MainActivity',
            'noReset': 'True',
            'fullReset': 'false'
        }
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)

    def test_01(self):
        u"""登录"""
        driver = self.driver
        self.driver.implicitly_wait(10)

        driver.find_element_by_id("com.vivachek.nova.tnineeightzeroone:id/etHisId").send_keys("1810")

        driver.find_element_by_id('com.vivachek.nova.tnineeightzeroone:id/etPassword').send_keys("123456")

        driver.find_element_by_id("com.vivachek.nova.tnineeightzeroone:id/btnLogin").click()

    def teardown_class(self):
        self.driver.quit()

if __name__ == '__main__':
    print("----------执行---------- ")
    suite = unittest.TestSuite()  # 构造测试集
    suite.addTest(TestloginTest('testCase'))
    # 定义自动化报告目录



