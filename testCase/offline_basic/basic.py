import threading
import time
import os
import sqlite3
import shutil
import subprocess
import json,random

exec_count = 0
def heart_beat():

    print(time.strftime('%Y-%m-%d %H:%M:%S'))
    global exec_count
    exec_count += 1
    if exec_count < 5:
        threading.Timer(3, heart_beat).start()

def get_Nonce():
    number = random.randint(1000, 10000)
    return str(number)

def get_number():
    number = random.randint(1, 8)
    return number

def get_unixtime():
    local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    times = time.mktime(time.strptime(local_time, '%Y-%m-%d %H:%M:%S'))
    return str(int(times * 1000))

def cmd_test():
    path = r'C:\Users\zf\PycharmProjects\jiekou\data\databases'
    if os.path.exists(path):
        shutil.rmtree(path)
    p = subprocess.Popen("cmd.exe /c" + r"C:\Users\zf\PycharmProjects\jiekou\data\push.bat", stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    curline = p.stdout.readline()
    while (curline != b''):
        curline = p.stdout.readline()
    p.wait()

def get_update(list):
    print(list)




