# encoding utf-8
import os,re
import jenkins #安装pip install python-jenkins
import json
import urllib3


def get_realip():
    filename = "ip.swbd"
    # open(filename, "w").write("")
    os.system("ipconfig > {}".format(filename))
    text = open("{}".format(filename)).read()
    try:
        ipv4 = re.findall(r'以太网适配器 以太网:(.*?)默认网关', text, re.S)[0]
        ipv4 = re.findall(r'IPv4 地址 . . . . . . . . . . . . :(.*?)子网掩码', ipv4, re.S)[0].replace(" ", "")
    except:
        ipv4 = re.findall(r'无线局域网适配器 WLAN:(.*?)默认网关', text, re.S)[0]
        ipv4 = re.findall(r'IPv4 地址 . . . . . . . . . . . . :(.*?)子网掩码', ipv4, re.S)[0].replace(" ", "")
    os.remove(filename)
    return ipv4.strip()
jenkins_url= "http://"+get_realip()+':8080'

#获取jenkins对象
server = jenkins.Jenkins(jenkins_url, username='zf699976', password='zf699976') #Jenkins登录名 ，密码
# job名称
job_name = "job/allure" #Jenkins运行任务名称
# job的url地址
job_url = jenkins_url +'/'+ job_name
# 获取最后一次构建

job_last_number=server.get_info(job_name)['lastBuild']['number']
# print(job_last_number)
report_url = job_url+ "/"+str(job_last_number)+'/allure'
print(report_url)
'''
钉钉推送方法：
读取report文件中"prometheusData.txt"，循环遍历获取需要的值。
使用钉钉机器人的接口，拼接后推送text
'''

def DingTalkSend():
    d = {}
    # 获取项目绝对路径
    path = os.path.abspath(os.path.dirname((__file__)))

    # 打开prometheusData 获取需要发送的信息
    f = open(r'../report_allure/export/prometheusData.txt', 'r')
    for lines in f:
        for c in lines:
            launch_name = lines.strip('\n').split(' ')[0]
            num = lines.strip('\n').split(' ')[1]
            d.update({launch_name: num})
    print(d)
    f.close()
    retries_run = d.get('launch_retries_run')  # 运行总数
    print('运行总数:{}'.format(retries_run))
    status_passed = d.get('launch_status_passed')  # 通过数量
    print('通过数量：{}'.format(status_passed))
    launch_status_broken = d.get('launch_status_broken')  # 损坏数量
    print('损坏数量：{}'.format(launch_status_broken))
    status_failed = d.get('launch_status_failed')  # 不通过数量
    print('失败数量：{}'.format(status_failed))

    # 钉钉推送

    url = 'https://oapi.dingtalk.com/robot/send?access_token=71f38c22c5d5afae79424f1ad748b01c9e53492cb839b059974a895951b20a02'  # webhook
    con = {"msgtype": "text",
           "text": {
               "content": "微策云小助手"
                          "\n测试概述:"
                          "\n运行总数:" + retries_run +
                          "\n通过数量:" + status_passed +
                          "\n警告数量:" + launch_status_broken +
                          "\n失败数量:" + status_failed +
                          "\n构建地址：\n" + job_url +
                          "\n报告地址：\n" + report_url
           }
           }
    urllib3.disable_warnings()
    http = urllib3.PoolManager()
    jd = json.dumps(con)
    jd = bytes(jd, 'utf-8')
    # print(jd)
    http.request('POST', url, body=jd, headers={'Content-Type': 'application/json'})
    print(type(http.request('POST', url, body=jd, headers={'Content-Type': 'application/json'})))

if __name__ == '__main__':
    DingTalkSend()

l=['1','2','3']
print(",".join(l))