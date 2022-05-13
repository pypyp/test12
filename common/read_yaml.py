# coding=UTF-8
import os,sys
sys.path.append(r''+os.path.abspath('../'))
import yaml


def load(path):
    # open方法打开直接读出来
    f = open(path, 'r', encoding='utf-8')
    data = yaml.load(f,Loader=yaml.FullLoader)
    return data
# print(load('C:\\Users\zf\PycharmProjects\jiekou\data\inhos_patient\inhos_patient_update.yaml'))