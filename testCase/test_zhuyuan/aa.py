import os
import sys

sys.path.append(r'' + os.path.abspath('../../'))
import requests,pymysql,random,datetime

time='2022-01-01 08:30:30'


conn = pymysql.connect(host='47.111.0.135',user = "root",passwd = "Nov2014",db = "vivachek_cloud2.2.0")

cursor = conn.cursor()
sql = 'SELECT sn,inhos_dept_id FROM `dev_info` where `status`=1 AND hos_id=1'
cursor.execute(sql)
results = cursor.fetchall()
for row in results:
    sn = row[0]
    dept_id = row[1]
    if dept_id!=None:
        sql = 'SELECT his_id FROM `user_info` where `status`=1 AND hos_id=1'
        cursor.execute(sql)
        nurse = cursor.fetchall()
        his_id = random.choice(nurse)[0]
        for i in range(2):
            print(sn,his_id,str(round(random.uniform(10, 30),1)))