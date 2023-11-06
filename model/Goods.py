from util.SqliteClient import SqliteClient


class Goods:
    columns = ('name', 'weight', 'g', 'price', 'remark')
    tablename = 'goods'

    def getConnection(self):
        return SqliteClient.getConnection()

    def insert(self, **insert):
        return SqliteClient.insert(self.tablename, **insert)

    def batchInsert(self, data):
        return SqliteClient.batchInsert(self.tablename, self.columns, data)
