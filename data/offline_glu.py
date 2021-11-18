import json, sqlite3
from testCase.offilne import sqlite

analysis = {}
def get_analysisModel(analysisModel):
    analysis['id'] = analysisModel




def glu_upload():
    sql = """select * from glucose where type = 1 """
    data1 = sqlite().select_type(sql)
    l = []

    for i in data1:
        dict = {}
        dict["userId"] = i[3],
        dict["nurseId"] = i[16],
        dict["deviceNo"] = i[12],
        dict["timeType"] = i[8],
        dict["measureTime"] = i[14],
        dict["comment"] = i[20],
        dict["method"] = i[13],
        dict["status"] = i[21],
        dict["unusual"] = i[15],
        dict["value"] = i[11],
        dict["valueUnit"] = i[18],
        dict["paperNum"] = (1,)
        for key,value in dict.items():
            dict[key] = value[0]
        l.append(dict)
    dd = {
        "analysisModel": analysis['id'],
        "measures":l
    }
    return dd

def qc_upload():
    sql = """select * from quality_control where remote = 1 """
    data1 = sqlite().select_type(sql)

    l = []
    for i in data1:
        dict = {}
        dict["value"] = i[2],
        dict["sn"] = i[3],
        dict["result"] = i[4],
        dict["measureTime"] = i[5],
        dict["operatorUserId"] = i[7],
        dict["deptId"] = i[8],
        dict["paperId"] = i[10],
        dict["paperOpenTime"] = i[11],
        dict["liquidId"] = i[15],
        dict["liquidOpenTime"] = i[17],
        dict["status"] = i[24],
        dict["paperNum"] = (1,)

        for key, value in dict.items():
            dict[key] = value[0]
        l.append(dict)
    return l
def external_upload():
    sql = """select * from external_quality_assessment where type = 1 """
    data1 = sqlite().select_type(sql)
    l = []
    for i in data1:
        dict = {}
        dict["sn"] = i[2],
        dict["measureTime"] = i[3],
        dict["batchNum"] = i[4],
        dict["sampleNum"] = i[5],
        dict["value"] = i[6],
        dict["nurseId"] = i[7],
        dict["status"] = i[8],

        for key, value in dict.items():
            dict[key] = value[0]
        l.append(dict)
    return l


def compare_upload():
    sql = """select * from compare_test_record where remote = 0 """
    data1 = sqlite().select_type(sql)
    l = []
    for i in data1:
        dict = {}
        dict["result"] = i[2],
        dict["detectionTime"] = i[4],
        dict["paperId"] = i[5],
        dict["sampleNo"] = i[8],
        dict["unusual"] = i[3],
        dict["operatorUserId"] = i[7],
        dict["sn"] = ('359A00004C2',0)

        for key, value in dict.items():
            dict[key] = value[0]
        l.append(dict)
    return l