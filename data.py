from util.pool import mysqlPool


class Data:
    @staticmethod
    def search(tablename='', where="", start=0, limit=30, order="id desc"):
        print(start, limit)
        if not tablename:
            raise Exception("缺少表名")

        count = 0
        list = []
        sql = "select * from {}".format(tablename)
        if where:
            sql = sql + " where " + where
        if order:
            sql = sql + " order by " + order
        sql = sql + " limit %s,%s"
        conn = mysqlPool.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, ((start - 1) * limit, limit,))
        for row in cursor.fetchall():
            list.append(row)

        cursor.close()
        conn.close()

        if start <= 1:
            sql = "SELECT count(1) FROM {}".format(tablename)
            if where:
                sql = sql + " where " + where
            conn = mysqlPool.get_connection()
            cursor = conn.cursor()
            cursor.execute(sql)
            count = cursor.fetchone()[0]
            cursor.close()
            conn.close()
        return {
            'list': list,
            'count': count
        }

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
    def deleteByPk(table, id):
        sql = "delete from %s where id=%d"
        conn = mysqlPool.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (table, id))
        conn.commit()
        cursor.close()
        conn.close()
