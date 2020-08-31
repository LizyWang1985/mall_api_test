import pymysql
from config.config import *

class DB:
    def __init__(self):
        self.conn=pymysql.connect(host=host,port=port,user=user,passwd=passwd,db=db,charset='utf8') # passwd 不是 password  # 如果查询有中文，需要指定测试集编码
        self.cur=self.conn.cursor()

    def __del__(self):# 析构函数，实例删除时触发
        self.cur.close()
        self.conn.close()

    def query(self,sql):
        logging.debug(sql)  #输出执行的sql
        self.cur.execute(sql)
        return self.cur.fetchall()

    def exec(self,sql):
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logging.error(str(e)) #输出错误信息

    # def check_Subject_List(self,keyword,pageNum,pageSize):
    #     limita = (pageNum-1)*pageSize #sql语句中不运算所以提出来运算完毕再使用
    #     sql= 'SELECT title FROM cms_subject WHERE title LIKE "%{}%"  limit {},{};'.format(keyword,limita,pageSize)
    #     print(sql)
    #     result = self.query(sql)
    #     return result
    #
    # def check_Subject_List_total(self,keyword,pageNum,pageSize):
    #     limita = (pageNum-1)*pageSize #sql语句中不运算所以提出来运算完毕再使用
    #     sql= 'SELECT count(title) FROM cms_subject WHERE title LIKE "%{}%"  limit {},{};'.format(keyword,limita,pageSize)
    #     print(sql)
    #     result = self.query(sql)
    #     return result

    def check_user(self,name):
        result=self.query("select * from EMPLOYEE where FIRST_NAME='{}'".format(name))
        return True if result else False

    def add_user(self,FIRST_NAME):
        self.exec("INSERT INTO EMPLOYEE (FIRST_NAME,LAST_NAME,AGE,SEX,INCOME)VALUES(FIRST_NAME,'Tomas',30,'W',3500);")

    def del_user(self,name):
        self.exec("delete from EMPLOYEE where FIRST_NAME='{}'".format(name))

# if __name__ == '__main__':
#     db=DB()
#     if db.check_user("Lizy"):
#         db.del_user("Lizy")





