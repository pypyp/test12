import json
class paper_info:
    def paper_info(self):  # 查询试纸
        data = json.dumps({
            "pageNo": 1,
            "pageSize": 20
        })
        return data
    def paper_add(self):  # 添加试纸
        data = json.dumps({
            "specs": 0,
            "paperNum": 20,
            "productionDate": "2018-09-01",
            "expiryDate": "2022-09-01",
            "lowMaxLimit": "50",
            "lowMinLimit": "2",
            "mediumMaxLimit": "40",
            "mediumMinLimit": "3",
            "highMaxLimit": "30",
            "highMinLimit": "6",
            "batchNum": "2019020231"
        })
        return data

    def paper_select(self):  # 添加试纸
        data = json.dumps({
            "pageNo": 1,
            "pageSize": 15
        })
        return data


    def paper_select_mh(self):  # 添加试纸
        data = json.dumps({
            "pageNo": 1,
            "pageSize": 15,
            "batchNum": "20"
        })
        return data


