from util.Pool import getSqliteConn
from util.Logger import logger
import sqlite3


class SqliteClient:
    @staticmethod
    def getConnection():
        return getSqliteConn()

    @staticmethod
    def _exec(sql, fetch='all', params=None, **kwargs):
        conn = getSqliteConn()
        cursor = conn.cursor()
        cursor.execute(sql, params)

        fetchFuncList = {
            "all": SqliteClient.fetchall,
            "one": SqliteClient.fetchone,
        }
        if fetch not in fetchFuncList:
            raise Exception("fetch参数错误")

        list = fetchFuncList[fetch](cursor, **kwargs)
        cursor.close()
        conn.close()
        return list

    @staticmethod
    def dataList(tablename='', field='*', where="", start=1, limit=30, order="id desc"):
        if not tablename:
            raise Exception("缺少表名")

        count = 0
        sql = "select {} from {}".format(field, tablename)
        args = ()
        if where:
            whereString, whereArgs = SqliteClient.buildWhere(where)
            sql += " where {}".format(whereString)
            args += whereArgs
        if order:
            sql = sql + " order by " + order
        sql = sql + " limit %s,%s"
        args += ((start - 1) * limit, limit,)
        list = SqliteClient._exec(sql, params=args)

        if start <= 1:
            sql = "SELECT count(1) FROM {} {}".format(tablename, 'limit 1')
            if where:
                sql = sql + " where " + where
            count = SqliteClient._exec(sql, fetch='one', column=0)
        return {
            'list': list,
            'count': count
        }

    def select(tablename='', field='*', where='', order='id desc', start=1, limit=10):

        sql = "select {} from {} ".format(field, tablename)
        args = ()
        if where:
            whereString, whereArgs = SqliteClient.buildWhere(where)
            sql += " where {}".format(whereString)
            args += whereArgs
        if order:
            sql += " order by " + order
        sql += " limit %s,%s"
        args += ((start - 1) * limit, limit,)
        return SqliteClient._exec(sql, params=args)

    @staticmethod
    def one(tablename='', field='*', where='', order='id desc'):
        sql = "select {} from {} ".format(field, tablename)
        args = ()
        if where:
            whereString, whereArgs = SqliteClient.buildWhere(where)
            sql += " where {}".format(whereString)
            args += whereArgs
        sql += " order by " + order + " limit 1"
        return SqliteClient._exec(sql, fetch='one', params=args)

    @staticmethod
    def all(tablename='', where="", order="id desc"):
        if not tablename:
            raise Exception("缺少表名")

        args = ()
        sql = "select * from {}".format(tablename)
        if where:
            whereString, whereArgs = SqliteClient.buildWhere(where)
            sql += " where {}".format(whereString)
            args += whereArgs
        if order:
            sql += " order by {}".format(order)
        list = SqliteClient._exec(sql, params=args)
        return {
            'list': list,
            'count': len(list)
        }

    @staticmethod
    def count(tablename, where=""):
        if not tablename:
            raise Exception("缺少表名")
        args = ()
        sql = "select count(1) from {} ".format(tablename)
        if where:
            whereString, whereArgs = SqliteClient.buildWhere(where)
            sql += " where {}".format(whereString)
            args += whereArgs
        return SqliteClient._exec(sql, fetch='one', column=0, params=args)

    @staticmethod
    def insert(tablename, **kwargs):
        if not tablename:
            raise Exception("缺少表名")
        keys = list(kwargs.keys())
        values = list(kwargs.values())
        sql = "insert into {} ({}) values ({})".format(tablename, ','.join(keys), ','.join(['?'] * len(values)))
        conn = getSqliteConn()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        lastInertId = cursor.lastrowid
        cursor.close()
        conn.close()
        return lastInertId

    @staticmethod
    def batchInsert(tablename, columns, data):
        if not tablename:
            raise Exception("缺少表名")
        keys = columns
        sql = "insert into {} ({}) values ({})".format(tablename, ','.join(keys), ','.join(['?'] * len(columns)))
        conn = getSqliteConn()
        cursor = conn.cursor()
        cursor.execute('BEGIN TRANSACTION')
        try:
            cursor.executemany(sql, data)
        except sqlite3.Error as e:
            print(e)
            logger.error("Sqlite插入数据时发生错误:%s" % e)
            # 回滚事务
            conn.rollback()
            return False
        conn.commit()
        cursor.close()
        conn.close()
        return True

    @staticmethod
    def update(tablename, where='', **kwargs):
        if not tablename:
            raise Exception("缺少表名")
        keys = list(kwargs.keys())
        values = tuple(list(kwargs.values()))
        sql = "update {} set {} ".format(tablename, ','.join(['{}=?'.format(key) for key in keys]))
        if where:
            whereString, whereArgs = SqliteClient.buildWhere(where)
            sql += " where {}".format(whereString)
            values = values + whereArgs
        conn = getSqliteConn()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        modifyLine = cursor.total_changes
        conn.close()
        cursor.close()
        return modifyLine

    @staticmethod
    def deleteByPk(table, id):
        sql = "delete from {} where id={}".format(table, id)
        conn = getSqliteConn()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        changeLine = conn.total_changes
        cursor.close()
        conn.close()
        return changeLine

    @staticmethod
    def delete(tablename, where=''):
        if not tablename:
            raise Exception("缺少表名")
        args = ()
        sql = "delete from {} ".format(tablename)
        if where:
            whereString, whereArgs = SqliteClient.buildWhere(where)
            sql += " where {}".format(whereString)
            args += whereArgs
        conn = getSqliteConn()
        cursor = conn.cursor()
        cursor.execute(sql, args)
        changeLine = conn.total_changes
        cursor.close()
        conn.close()
        return changeLine

    @staticmethod
    def fetchone(cursor, **kwargs):
        if 'column' in kwargs:
            return cursor.fetchone()[kwargs['column']]
        else:
            return cursor.fetchone()

    @staticmethod
    def fetchall(cursor, **kwargs):
        return cursor.fetchall()

    @staticmethod
    def buildWhere(where):
        whereArgs = []
        whereString = ""

        if isinstance(where, dict):
            whereArgs = list(where.values())
            whereString = " AND ".join(["{}=%s".format(key) for key in where.keys()])

        elif isinstance(where, list):
            for item in where:
                if isinstance(item, str):
                    whereString += "{} AND ".format(item)
                elif isinstance(item, dict):
                    key = list(item.keys())[0]
                    value = list(item.values())[0]
                    whereString += "{} = %s AND ".format(key)
                    whereArgs.append(value)
                elif len(item) > 3:
                    whereString += "{} {} %s AND %s ".format(item[1], item[0])
                    whereArgs.extend(item[2:])
                elif len(item) > 2:
                    whereString += "{} {} %s AND ".format(item[0], item[1])
                    whereArgs.append(item[2])
                else:
                    whereString += "{} = %s AND ".format(item[0])
                    value = item[1]
                    if value:
                        whereArgs.append(value)

        elif isinstance(where, str):
            whereString = where

        return whereString.rstrip('AND '), tuple(whereArgs)
