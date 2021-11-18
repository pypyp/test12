import json
class liquid:


    def liquid_info(self):  # 查询质控液
        data = json.dumps({
            "pageNo": 1,
            "pageSize": 20
        })
        return data


    def liquid_add(self):  # 添加质控液
        data = json.dumps({
            "specs": 0,
            "liquidNum": 20,
            "type": 0,
            "productionDate": "2018-09-01",
            "expiryDate": "2022-09-01",
            "batchNum": "2019020231"
        })
        return data


    def liquid_select(self):  # 添加质控液
        data = json.dumps({
            "pageNo": 1,
            "pageSize": 15
        })
        return data



    def liquid_select_mh(self):  # 添加质控液
        data = json.dumps({
            "pageNo": 1,
            "pageSize": 15,
            "batchNum": "20"
        })
        return data