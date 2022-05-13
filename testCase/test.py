# coding=UTF-8
"""
#autho:zf
#describle:为甜甜专属制作
"""
import datetime, time, data
import xlrd, requests
from xlutils.copy import copy
from testCase.offline_basic.sqlite import sqlite
import random

def change():
    l = []
    measureTime = '2022-04-01 00:00:00'
    sql=""" select * from analysis_task """
    task = sqlite().select_id(sql)

    for i in task:
        dict={}
        dict['measureId']=i[1]
        dict['userId'] =i[2]
        dict['iptNum'] = i[3]
        dict['name']=i[4]
        dict['deptid']=i[9]
        dict['type']=i[24]
        dict['bedsort']=i[-2]
        l.append(dict)
    return l



def insrt():
    l=[]
    l1=[]
    l2=[]
    measureTime='2022-04-08 00:00:00'
    measureTime = (datetime.datetime.strptime(measureTime, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(
        minutes=2)).strftime("%Y-%m-%d %H:%M:%S")


    nurseId = '01224'
    deviceNo = '359B0000064'
    value ='25.5'
    for i in range(2):
        dict = {}
        dict["measureTime"] = measureTime
        measureTime = (datetime.datetime.strptime(measureTime, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(
            minutes=1)).strftime("%Y-%m-%d %H:%M:%S")
        dict['userId'] = '000168441300'
        dict['nurseId'] = nurseId
        dict['deviceNo'] = deviceNo
        dict['timeType'] = '早餐后'
        dict['comment'] = ''
        dict['status'] = 1
        dict['unusual'] = 1
        dict['paperNum'] = 1
        dict["valueUnit"] = 1
        measureTime = (datetime.datetime.strptime(measureTime, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(
            minutes=2)).strftime("%Y-%m-%d %H:%M:%S")
        dict["measureTime"] = measureTime
        dict["value"] = value
        l.append(dict)

    for i in range(2):
        dict = {}
        dict["measureTime"] = measureTime
        measureTime = (datetime.datetime.strptime(measureTime, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(
            minutes=1)).strftime("%Y-%m-%d %H:%M:%S")
        dict['nurseId'] = nurseId
        dict['deviceNo'] = deviceNo
        dict['timeType'] = '早餐后'
        dict['comment'] = ''
        dict['status'] = 1
        dict['unusual'] = 1
        dict['paperNum'] = 1
        dict["valueUnit"] = 1
        measureTime = (datetime.datetime.strptime(measureTime, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(
            minutes=2)).strftime("%Y-%m-%d %H:%M:%S")
        dict["measureTime"] = measureTime
        dict["value"] = value
        l1.append(dict)

    task =change()


    for i in task:
        if i['type'] =='晚餐后':
            dict = {}
            dict["measureTime"] = measureTime
            measureTime = (datetime.datetime.strptime(measureTime, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(
                minutes=1)).strftime("%Y-%m-%d %H:%M:%S")
            dict['measureId'] =i['measureId']
            dict['userId'] = '000168441300'
            dict['nurseId'] = nurseId
            dict['deviceNo'] = deviceNo
            dict['timeType'] = i['type']
            dict['comment'] = ''
            dict['status'] = 1
            dict['unusual'] = 1
            dict['paperNum'] = 1
            dict["valueUnit"] = 1
            measureTime = (datetime.datetime.strptime(measureTime, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(
                minutes=2)).strftime("%Y-%m-%d %H:%M:%S")
            dict["measureTime"] = measureTime
            dict["value"] = value
            l.append(dict)
            l2.append(i['measureId'])




    dd = {
        "analysisModel": 1,
        "measures": l,
        "tempMeasures":l1
    }


    dd1 = {
            "analysisModel": 1,
            "completeSingleMeasureList": l2
        }

    return dd ,dd1


# print(insrt())

def aa():
    measureTime = '2022-04-12 00:00:00'
    value=str(round(random.uniform(2, 33),1))
    deviceNo = '359B0000064'
    for i in range(40):
        sql = """INSERT INTO "glucose"
                   ("uid", "id", "measureId", "userId", "iptNum", "deptId", "name", "bedNum", "timeType", "timeSlot", "measureType", "value", "deviceNo", "method", "measureTime", "unusual", "nurseId", "nurseName", "valueUnit", "updateTime", "comment", "status", "type", "color", "bedSort")
                   VALUES (NULL, NULL, NULL, '000168441300', '793905', '1060100', '吴伟忠', '1026', '午餐后', '午餐后', 1, \'{}\', '359B0000064', 1, \'{}\', 0, '551796274966298624', 'fff', 1, NULL, '', 1, 1, 2, '')""".format(value,measureTime);
        sqlite().insert(sql)
        measureTime = (datetime.datetime.strptime(measureTime, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(
            minutes=2)).strftime("%Y-%m-%d %H:%M:%S")


    for i in range(40):
        sql = """INSERT INTO "glucose"
                   ("uid", "id", "measureId", "userId", "iptNum", "deptId", "name", "bedNum", "timeType", "timeSlot", "measureType", "value", "deviceNo", "method", "measureTime", "unusual", "nurseId", "nurseName", "valueUnit", "updateTime", "comment", "status", "type", "color", "bedSort")
                   VALUES (NULL, NULL, NULL, NULL, NULL, '1060100', NULL, NULL, '午餐后', '午餐后', 1, \'{}\', '359B0000064', 1, \'{}\', 0, '551796274966298624', 'fff', 1, NULL, '', 1, 3, 2, '')""".format(value,measureTime);
        sqlite().insert(sql)
        measureTime = (datetime.datetime.strptime(measureTime, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(
            minutes=2)).strftime("%Y-%m-%d %H:%M:%S")

    task = change()
    type1='晚餐前'
    type2='晚餐后'
    sql = """update analysis_task set close=1 where filterTimeType=\'{}\'""".format(type1)
    sqlite().insert(sql)
    sql = """update analysis_task set close=1 where filterTimeType=\'{}\'""".format(type2)
    sqlite().insert(sql)
    for i in task:
        if i['type'] == type1 or i['type'] == type2:
            sql = """INSERT INTO "glucose"
                           ("uid", "id", "measureId", "userId", "iptNum", "deptId", "name", "bedNum", "timeType", "timeSlot", "measureType", "value", "deviceNo", "method", "measureTime", "unusual", "nurseId", "nurseName", "valueUnit", "updateTime", "comment", "status", "type", "color", "bedSort")
                           VALUES (NULL, NULL,\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', 1, \'{}\', '359B0000064', 1, \'{}\', 0, '551796274966298624', 'fff', 1, NULL, '', 1, 2, 2, \'{}\')"""\
                .format(i['measureId'],i['userId'],i['iptNum'],i['deptid'],i['name'],i['bedsort'],i['type'],i['type'],value,measureTime,i['bedsort'])
            sqlite().insert(sql)
            measureTime = (datetime.datetime.strptime(measureTime, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(
                minutes=2)).strftime("%Y-%m-%d %H:%M:%S")

    # dd = {
    #     "analysisModel": 0,
    #     "measures": l
    # }
    # return dd
print(aa())

def read_excel():
    wb = xlrd.open_workbook(r'.xlsx')
    # sheet1索引从0开始，得到sheet1表的句柄
    new_book = copy(wb)
    new_sheet = new_book.get_sheet(0)

    sheet = wb.sheet_by_index(0)
    rowNum = sheet.nrows
    colNum = sheet.ncols
    print(rowNum, colNum)

    # 打开文件
    wb1 = xlrd.open_workbook(r'C:\Users\zf\PycharmProjects\jiekou\testCase\12.16粉象线下面膜等等.xls')
    # 获取所有sheet的名字
    sheet1 = wb1.sheet_by_index(0)
    rowNum1 = sheet1.nrows
    colNum1 = sheet1.ncols
    print(rowNum1, colNum1)

    for i in range(1, rowNum):
        a = int(sheet.cell(i, 2).value)
        for j in range(1, rowNum1):
            if int(sheet1.cell(j, 0).value) == a:
                new_sheet.write(i, 16, sheet1.cell(j, 1).value)
    new_book.save('book.xlsx')



    # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # print(change())
    # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
