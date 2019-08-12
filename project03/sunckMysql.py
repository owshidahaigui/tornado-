import pymysql

class SunckMySQL():

    def __init__(self, host, user, passwd, dbName):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.dbName = dbName

    def connet(self):
        self.db = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.passwd,
            database=self.dbName)
        self.cursor = self.db.cursor()

    def close(self):
        self.cursor.close()
        self.db.close()

    def get_one(self, sql):
        res = None
        try:
            self.connet()
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
            self.close()
        except:
            print('查询失败')
        return res

    def get_all(self, sql):
        res = ()
        try:
            self.connet()
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            self.close()
        except:
            print('查询失败')
        return res

    #推荐使用，返回字典列表
    def get_all_obj(self, sql, tableName, *args):
        reslist = []
        fieldsList = []
        if (len(args) > 0):
            for item in args:
                fieldsList.append(item)
        else:
            fieldsSql = "select COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS where table_name = '%s' and TABLE_SCHEMA= '%s'" % (
                tableName, self.dbName)
            fields = self.get_all(fieldsSql)
            for item in fields:
                fieldsList.append(item[0])
        # 执行查询数据sql
        res = self.get_all(sql)
        for item in res:
            obj = {}
            count = 0
            for x in item:
                obj[fieldsList[count]] = x
                count += 1
            reslist.append(obj)
        return reslist

    def insert(self, sql):
        return self.__edit(sql)

    def update(self, sql):
        return self.__edit(sql)

    def delete(self, sql):
        return self.__edit(sql)

    def __edit(self, sql):
        count = 0
        try:
            self.connet()
            count = self.cursor.execute(sql)
            self.db.commit()
            self.close()
        except:
            print('事物提交失败')
            self.db.rollback()
        return count
