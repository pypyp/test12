import json,time



class qc_record:
    def qc_record(self):  # 查询试纸
        data = json.dumps({
            "pageNo": 1,
            "pageSize": 20
        })
        return data


    def qc_add(self):  # 添加试纸
        data = {
            "value": 15.3,
            "sn": "359B0000357",
            "measureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),

            "result": 0,
        }
        return data

    def qc_select(self):  #
        data = json.dumps({
            "pageNo": 1,
            "pageSize": 15
        })
        return data


    def qc_select1(self):  #
        data = json.dumps({
            "pageNo": 1,
            "pageSize": 15,
            "sn": "359B0000357"
        })
        return data

    def qc_select2(self):  #
        data = json.dumps({
            "pageNo": 1,
            "pageSize": 15,
            "result": "0"
        })
        return data

    def qc_select3(self):  #
        data = json.dumps({
            "pageNo": 1,
            "pageSize": 15,
            "type": 0
        })
        return data


