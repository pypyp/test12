# Author xuejie zeng
# encoding utf-8
# content of test_demo.py

import pytest
import allure
import os
class TestDemo:

    @allure.story("测试")
    def test_a(self):
        print("a")
    b=2
    @pytest.mark.parametrize('a',['1'])
    def test_b(self,login,a):
        print("b")
    def test_c(self):
        print("c")
    def test_d(self):
        print("d")





if (__name__ == "__main__"):
    pytest.main(["-s",'test_01.py','--alluredir','/usr/local/pyTest/result'])
    print('1')
    os.system('allure generate /usr/local/pyTest/result -o /usr/local/pyTest/report_allure --clean')

