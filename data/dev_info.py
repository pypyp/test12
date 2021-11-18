import json
from common.yaml_util import read_yaml
from common.open_database import MysqlDb
from common.yaml_util import read_yaml, read_zy_yaml, read_bastase_sql, read_url_csv
class dev:
    global dept_id
    try:
        dept_id = read_yaml('deptId')

    except:
        data = MysqlDb().select_db(
            "select * from {}.`dept_info` where hos_id =\'{}\'".format(read_bastase_sql()[4], read_yaml('hosId')))
        dept_id = data[0]['id']

    def dev_info(self):  # 查询设备
        data = json.dumps({
            "pageNo": 1,
            "pageSize": 20
        })
        return data

    def device_add(self):  # 添加设备
        data = json.dumps({
            "bindModule": 0,
            "contrastTest": 0,
            "devQuality": 0,
            "devStatus": 0,
            "enableAdb": 1,
            "enableMtk": 0,
            "enableTouchFeedback": 0,
            "externalQuality": 0,
            "inhosDeptId": dept_id,
            "sn": "359B0000357",
            "uploadMtk": 0
        })
        return data

    def dev_select(self):  # 查询设备
        data = json.dumps({
            "pageNo": 1,
            "pageSize": 15
        })
        return data

    def dev_select1(self):  # 查询设备
        data = json.dumps({
            "pageNo": 1,
            "pageSize": 15,
            "inhosDeptId": dept_id

        })
        return data


    def dev_select_mh(self):  # 查询设备
        data = json.dumps({
            "pageNo": 1,
            "pageSize": 15,
            "sn": "359B"
        })
        return data