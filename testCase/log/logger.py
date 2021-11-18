# coding=UTF-8
import datetime
import logging.handlers
import os
from os.path import dirname


def getlogger():
    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG)
    path = os.path.abspath(dirname(dirname(dirname(__file__))) + '\\log')
    # path = 'C:\\Users\\zf\\PycharmProjects\\jiekou\\log'
    all = path + '\\' + 'all.log'
    error = path + '\\' + 'error.log'
    print(all, error)
    rf_handle = logging.handlers.TimedRotatingFileHandler(all, when='MIDNIGHT', interval=1, backupCount=7,
                                                          atTime=datetime.time(0, 0, 0, 0))
    rf_handle.setFormatter(logging.Formatter('%(asctime)s-%(levelname)s-%(module)s-%(message)s'))

    f_handle = logging.FileHandler(error)
    f_handle.setLevel(logging.WARNING)
    f_handle.setFormatter(logging.Formatter('%(asctime)s-%(levelname)s-%(filename)s[:%(lineno)d-%(message)s]'))

    logger.addHandler(rf_handle)
    logger.addHandler(f_handle)
    return logger
