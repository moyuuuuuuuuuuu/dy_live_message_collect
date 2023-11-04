from util.pool import mysqlPool


class MysqlClient:

    @staticmethod
    def _exec(sql, fetch='all', params=None, **kwargs):

        list = []
        conn = mysqlPool.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, params)

        fetchFuncList = {
            "all": MysqlClient.fetchall,
            "one": MysqlClient.fetchone,
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
        if where:
            sql = sql + " where " + where
        if order:
            sql = sql + " order by " + order
        sql = sql + " limit %s,%s"

        list = MysqlClient._exec(sql, params=((start - 1) * limit, limit,))

        if start <= 1:
            sql = "SELECT count(1) FROM {} {}".format(tablename, 'limit 1')
            if where:
                sql = sql + " where " + where
            count = MysqlClient._exec(sql, fetch='one', column=0)
        return {
            'list': list,
            'count': count
        }

    def select(tablename='', field='*', where='', order='id desc', start=1, limit=10):

        sql = "select {} from {} ".format(field, tablename)
        if where:
            sql += " where " + where
        if order:
            sql += " order by " + order
        sql += " limit %s,%s"

        return MysqlClient._exec(sql, params=((start - 1) * limit, limit,))

    @staticmethod
    def one(tablename='', field='*', where='', order='id desc'):
        sql = "select {} from {} ".format(field, tablename)
        if where:
            sql += " where " + where
        sql += " order by " + order + " limit 1"
        return MysqlClient._exec(sql, fetch='one')

    @staticmethod
    def all(tablename='', where="", order="id desc"):
        if not tablename:
            raise Exception("缺少表名")

        list = []
        sql = "select * from {}".format(tablename)
        if where:
            sql = sql + " where " + where
        if order:
            sql = sql + " order by " + order
        conn = mysqlPool.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        for row in cursor.fetchall():
            list.append(row)

        cursor.close()
        conn.close()
        return {
            'list': list,
            'count': len(list)
        }

    @staticmethod
    def count(tablename, where=""):
        if not tablename:
            raise Exception("缺少表名")
        sql = "select count(1) from {} ".format(tablename)
        if where:
            sql += " where " + where
        return MysqlClient._exec(sql, fetch='one', column=0)

    @staticmethod
    def deleteByPk(table, id):
        sql = "delete from %s where id=%d"
        conn = mysqlPool.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (table, id))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def fetchone(cursor, **kwargs):
        if 'column' in kwargs:
            return cursor.fetchone()[kwargs['column']]
        else:
            return cursor.fetchone()

    @staticmethod
    def fetchall(cursor, **kwargs):
        return cursor.fetchall()
