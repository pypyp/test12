# coding=UTF-8
import os,sys
import time
import random,json,datetime
sys.path.append(r''+os.path.abspath('../'))
class Ran():

    def phoneNORandomGenerator(self):
        prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152",
                   "153",
                   "155", "156", "157", "158", "159", "186", "187", "188"]
        return random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))
    def number(self):
        number = random.randint(1,500)
        return number
    def ran(self):
        #  随机生成年月日
        yea = random.randint(1933, int(time.strftime("%Y")))  # 生成年
        #  生成月
        mon = random.randint(1, 12)
        ran_mon = '0' + str(mon) if mon < 10 else mon
        #  生成日
        day = random.randint(1, 27)
        ran_day = '0' + str(day) if day < 10 else day
        return str(yea) + str(ran_mon) + str(ran_day)

    def ran_value(self):
        #  生成年月日后的三位数
        value = random.randint(10, 199)
        if value < 100:
            return "0" + str(value)
        else:
            return str(value)

    def ran_area(self):
        #  随机取生成前六位
        province = ('11', '12', '13', '14', '15', '21', '22', '23', '31', '32', '33', '34', '35', '36', '37', '41', '42',
                 '43', '44', '45', '46', '50', '51', '52', '53', '54', '61', '62', '63', '64', '65', '66')
        return str(province[random.randint(0, len(province))] + '0101')

    def ran_end(self):
        #  组成前17位数字
        ran = self.ran_area()+self.ran()+self.ran_value()
        #  前17位每位需要乘上的系数，用字典表示，比如第一位需要乘上7，最后一位需要乘上2
        coe = {1: 7, 2: 9, 3: 10, 4: 5, 5: 8, 6: 4, 7: 2, 8: 1, 9: 6, 10: 3, 11: 7, 12: 9, 13: 10, 14: 5, 15: 8, 16: 4,
               17: 2}
        summat = 0
        #  循环计算前17位每位乘上系数之后的和
        for i in range(17):
            summat = summat + int(ran[i:i + 1]) * coe[i + 1]
        #  前17位每位乘上系数之后的和除以11得到的余数对照表，比如余数是0，那第18位就是1
        mat = {0: '1', 1: '0', 2: 'X', 3: '9', 4: '8', 5: '7', 6: '6', 7: '5', 8: '4', 9: '3', 10: '2'}
        return ran + mat[summat % 11]

