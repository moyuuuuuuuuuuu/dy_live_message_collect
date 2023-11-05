import os.path

from util.MysqlClient import MysqlClient
from util.Pool import redisPool
from util.Exporter import Exporter
import redis, math, datetime, sys


def getRedisClient():
    return redis.Redis(connection_pool=redisPool)


class Logic:
    @staticmethod
    def liveMessageDataToExcel(item):
        # 获取直播间id
        # room_id = item.get("room_id")
        id, liveId, createdAt, numbers, isExcel, isWordCloud = item
        redisClient = getRedisClient()
        pushKey = 'dy:message:push:%s' % liveId
        listLength = redisClient.llen(pushKey)

        if listLength <= 0:
            return False, '远端无直播间id为[%s]的数据。请确认直播间id' % liveId
        limit = 1000  # 每批写入的行数
        num_batches = math.ceil(listLength / limit)  # 总批数
        filename = "%s-%s的直播弹幕数据" % (datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), liveId)
        export = Exporter(
            filename=filename,
            columns=['弹幕ID', '弹幕内容', '发布时间'])
        for i in range(num_batches):
            start = i * limit
            end = min((i + 1) * limit, listLength)

            messageIdList = redisClient.lrange(pushKey, start, end)
            pageData = []
            for id in messageIdList:
                key = "dy:message:hash:%s:%d" % (liveId, int(id))
                message = redisClient.hgetall(key)
                pageData.append(list(message.values()))
            export.append(data=pageData)
        export.save()
        MysqlClient.update('live', where={'id': id}, data={'is_excel': isExcel})
        return True, '导出成功'

    @staticmethod
    def liveMessageDataToWordCloud(item):
        pass
