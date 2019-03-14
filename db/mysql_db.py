import pymysql
from db.db_config import MySQLConfig
import base64


class MyMySQL:

    def __init__(self, host: str=None,
                 user: str=None,
                 password: str=None,
                 database: str=None,
                 port: int=3306,
                 charset='utf8mb4',
                 cursorclass=pymysql.cursors.DictCursor
                 ):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.charset = charset
        self.cursorclass = cursorclass

        self.connect = pymysql.connect(host=self.host,
                                          user=self.user,
                                          password=self.password,
                                          database=self.database,
                                          port=self.port,
                                          charset=self.charset,
                                          cursorclass=self.cursorclass
                                          )
        self.cursor = self.connect.cursor()


    def find_all(self, sql_statement: str, *args):
        """查询全部数据
        按照查询语句查询全部数据
        """
        result = None
        if self.connect.open:
            with self.connect.cursor() as sursor:
                try:
                    sursor.execute(sql_statement, args)
                    result = sursor.fetchall()
                except:
                    print('查询全部 出错')
                finally:
                    sursor.close()
        return result

    def find_many(self, sql_statement: str, size: int=None, *args):
        """查询多条数据
        按照查询语句查询多条数据，指定查询条数，默认查询一条
        """
        result = None
        if self.connect.open:
            with self.connect.cursor() as cursor:
                try:
                    cursor.execute(sql_statement, args)
                    result = cursor.fetchmany(size)
                except:
                    print('查询多条数据 出错')
                finally:
                    cursor.close()

        return result

    def find_one(self, sql_statement: str, *args):
        """查询单条数据
        按照查询语句查询单条数据
        """
        result = None
        if self.connect.open:
            with self.connect.cursor() as cursor:
                try:
                    cursor.execute(sql_statement, args)
                    result = cursor.fetchone()
                except:
                    print('查询单条数据 出错')
                finally:
                    cursor.close()
        return result

    def add_up_del(self, sql_statement: str, *args):
        """新增、更新和删除"""
        # sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        # cursor.execute(sql, ('webmaster@python.org', 'very-secret'))
        result = True
        if self.connect.open:
            with self.connect.cursor() as cursor:
                try:
                    cursor.execute(sql_statement, args)
                    self.connect.commit()
                except:
                    self.connect.rollback()
                    result = False
                    print('新增、更新和删除 出错')
                finally:
                    cursor.close()
        return result

    def add_up_del_mony(self, sql_statement: str, *args):
        """新增、更新和删除 多条数据"""
        result = True
        if self.connect.open():
            with self.connect.cursor() as cursor:
                try:
                    cursor.execute(sql_statement, args)
                    self.connect.commit()
                except:
                    self.connect.rollback()
                    result = False
                    print('新增、更新和删除多条数据 出错')
                finally:
                    cursor.close()
        return result

# 数据库连接
connect = MyMySQL(
                MySQLConfig.get_host(),
                MySQLConfig.get_user(),
                base64.b64decode(MySQLConfig.get_password()),
                MySQLConfig.get_database(),
            )


if __name__ == '__main__':

    # sql_str = 'select * from o_wechat_account'
    # # acc = connect.find_all(sql_str)
    # # acc = connect.find_many(sql_str, 2)
    # acc = connect.find_one(sql_str)
    # print(acc)

    sql = MyMySQL(user='root', password='lzmysql8', database='lz_cms', port=3307)
    db = sql.connect
    print(db)