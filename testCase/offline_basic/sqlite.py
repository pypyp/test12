import sqlite3
from testCase.log import logger
class sqlite():
    def __init__(self):
        self.conn = sqlite3.connect("C:\9801\databases\common.db")
        self.cur = self.conn.cursor()

    def __del__(self):  # 对象资源被释放时触发，在对象即将被删除时的最后操作
        # 关闭游标
        self.cur.close()
        # 关闭数据库连接
        self.conn.close()

    def select_offline_time(self):
        sql = """select * from common_update_time """
        self.cur.execute(sql)
        # 使用 fetchall() 获取查询结果
        data = self.cur.fetchone()
        return data

    def sqlite_update_time(self, sql):

        self.cur.execute(sql)
        # 使用 fetchall() 获取查询结果
        self.conn.commit()

    def insert(self, sql):

        self.cur.execute(sql)
        self.conn.commit()

    def delete(self, sql):

        self.cur.execute(sql)
        self.conn.commit()


    def select_type(self,sql):

        self.cur.execute(sql)
        # 使用 fetchall() 获取查询结果
        data = self.cur.fetchall()
        return data


    def select_id(self,sql):

        self.cur.execute(sql)
        # 使用 fetchall() 获取查询结果
        data = self.cur.fetchall()
        return data


    def select_gloucose_islogin(self, sql):

        self.cur.execute(sql)
        # 使用 fetchall() 获取查询结果
        data = self.cur.fetchall()
        return data

