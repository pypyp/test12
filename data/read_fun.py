# coding=UTF-8
import os, sys

sys.path.append(r'' + os.path.abspath('../'))
import jinja2
from common.read_yaml import load
from common.com import Ran
import time, datetime
import random
import testCase.get_basic as A
from datetime import timedelta

class Load_Basic():
    '''
    加载headers文件的内容包含登陆的账号信息，请求头 等
    '''
    @staticmethod
    def read_user_info():
        return load(load('../data/path/path.yaml')['basic']['header_path'])

    '''
    加载患者信息
    '''

    @staticmethod
    def read_patient_info():
        return load(load('../data/path/path.yaml')['basic']['inhos_patient_basic_info'])

    '''
    加载患者血糖信息
    '''

    @staticmethod
    def read_blood_info():
        return load(load('../data/path/path.yaml')['basic']['inhos_patient_blood_info'])

    '''
    加载医嘱信息
    '''

    @staticmethod
    def read_order_info():
        return load(load('../data/path/path.yaml')['basic']['order_info'])

    @staticmethod
    def read_temp_blood_info():
        return load(load('../data/path/path.yaml')['basic']['inhos_temp_info'])

    @staticmethod
    def read_sn_info():
        return load(load('../data/path/path.yaml')['basic']['sn_info'])


    @staticmethod
    def read_paper_info():
        return load(load('../data/path/path.yaml')['basic']['paper_info'])


    @staticmethod
    def read_liquid_info():
        return load(load('../data/path/path.yaml')['basic']['liquid_info'])


    @staticmethod
    def read_qc_info():
        return load(load('../data/path/path.yaml')['basic']['qc_info'])

    @staticmethod
    def read_mz_patient_info():
        return load(load('../data/path/path.yaml')['basic']['mz_patient_info'])


def render(tpl_path, **kwargs):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(loader=jinja2.FileSystemLoader(path or './')
                              ).get_template(filename).render(**kwargs)


# yaml 文件调用以下函数


'''
获取当前时间
'''


def get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


'''
获取当天0点和23:59
'''


def get_start_end_time():
    list = {}
    endTime = time.strftime("%Y-%m-%d 23:59:59", time.localtime())
    startTime = time.strftime("%Y-%m-%d 00:00:00", time.localtime())
    list['startTime'] = startTime
    list['endTime'] = endTime
    return list


'''
获取7天前的日期
'''


def start_time():
    yes_time_nyr = (datetime.datetime.now() + datetime.timedelta(days=-7)).strftime("%Y-%m-%d %H:%M:00")
    return yes_time_nyr





def read_basic_info():
    dict = {}
    dict['sn'] = Load_Basic.read_sn_info()
    dict['paper_info'] = Load_Basic.read_paper_info()
    dict['user_info'] = Load_Basic.read_user_info()
    dict['inhos_patient_info'] = Load_Basic.read_patient_info()
    dict['inhos_patient_blood_info'] = Load_Basic.read_blood_info()
    dict['inhos_temp_info'] = Load_Basic.read_temp_blood_info()
    dict['order_info'] = Load_Basic.read_order_info()
    dict['qc_info'] = Load_Basic.read_qc_info()

    return dict


'''
读取yaml文件
'''


def read_yaml_info(path):
    r = render(path,
               **{"phone": Ran().phoneNORandomGenerator, 'card': Ran().ran_end,
                  "get_time": get_time, "num": Ran().number, "get_start_end_time": get_start_end_time,
                  "start_time": start_time, 'qc_add': A.qc_record().qc_add,
                  'read_basic_info': read_basic_info})
    return r
