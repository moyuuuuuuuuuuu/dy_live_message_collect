#!/usr/bin/.env python
# -*- coding: utf-8 -*-

import math
import sys
import time
import datetime
import redis
import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from util.Pool import redisPool
from component.MessageFrame import MessageFrame
from tkinter import Text


class Spider():
    def __init__(self, liveId, master: MessageFrame):
        self.liveId = liveId
        self.master = master

    def getRedisClient(self):
        redis.Redis(connection_pool=redisPool)

    def visit(self, liveId=''):
        if not liveId:
            liveId = self.liveId
        pageUrl = "https://live.douyin.com/" + liveId

        option = Options()
        option.add_argument("--disable-extensions")  # 给option对象添加无头参数
        option.add_argument("--ignore-certificate-errors")  # 忽略证书异常错误
        option.set_capability("acceptInsecureCerts", True)

        web = Chrome(options=option)
        # web.minimize_window()  # 窗口最小化
        web.get(pageUrl)
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "启动了")
        time.sleep(10)
        while True:
            eles = web.find_elements(By.CLASS_NAME, 'webcast-chatroom___enter-done')

            if len(eles) > 0:
                for ele in eles:
                    redisConn = getRedis()
                    try:
                        es = ele.find_element(By.CLASS_NAME, 'webcast-chatroom___content-with-emoji-text')
                        id = ele.get_attribute('data-id')
                        hashKey = 'dy:message:hash:' + liveId + ':' + id

                        if not es or redisConn.exists(hashKey):
                            continue

                        pushKey = 'dy:message:push:' + liveId
                        redisConn.lpush(pushKey, id)

                        redisConn.hset(hashKey, 'id', id)
                        redisConn.hset(hashKey, 'content', es.text)
                        redisConn.hset(hashKey, 'time', int(time.time()))
                        print("%s-%s-%s" % (
                            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            ele.get_attribute('data-id'),
                            es.text))
                        Text(self.master, text="%s-%s-%s" % (
                            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            ele.get_attribute('data-id'),
                            es.text)).pack(fill='x')
                    except NoSuchElementException:
                        pass
                    except StaleElementReferenceException:
                        pass


def getRedis():
    return redis.Redis(connection_pool=redisPool)


def export(liveId, delRemoteData):
    print('开始导出...')
    redisClient = getRedis()
    pushKey = 'dy:message:push:' + liveId
    listLength = redisClient.llen(pushKey)

    if listLength <= 0:
        print('远端无直播间id为[' + liveId + ']的数据。请确认直播间id')
        sys.exit(0)
    limit = 1000  # 每批写入的行数
    num_batches = math.ceil(listLength / limit)  # 总批数
    writer = pd.ExcelWriter(liveId + '.xlsx', engine='xlsxwriter')  # 创建一个 E
    for i in range(num_batches):
        start = i * limit
        end = min((i + 1) * limit, listLength)

        messageIdList = redisClient.lrange(pushKey, start, end)
        messageMap = {"弹幕ID": [], "弹幕内容": [], "发布时间": []};
        for id in messageIdList:
            key = "dy:message:hash:" + liveId + ":%d" % int(id)
            messageMap['弹幕ID'].append("%d" % int(redisClient.hget(key, 'id')))
            messageMap['弹幕内容'].append(redisClient.hget(key, 'content').decode('UTF-8'))
            messageMap['发布时间'].append(str(datetime.datetime.fromtimestamp(int(redisClient.hget(key, 'time')))))

        df = pd.DataFrame(messageMap)
        df.set_index('弹幕ID')
        df.to_excel(writer, sheet_name='Sheet1', index=False, startrow=start)
    writer._save()
    print('导出完毕,可查看文件')
    if delRemoteData:
        delData(liveId)


def delData(liveId):
    print('正在远端清除数据,程序执行完毕将自动终止')
    redisClient = getRedis()
    pushKey = 'dy:message:push:' + liveId
    listLength = redisClient.llen(pushKey)
    limit = 1000  # 每批写入的行数
    num_batches = math.ceil(listLength / limit)  # 总批数
    for i in range(num_batches):
        start = i * limit
        end = min((i + 1) * limit, listLength)
        messageIdList = redisClient.lrange(pushKey, start, end)
        for messageId in messageIdList:
            key = "dy:message:hash:" + liveId + ":%d" % int(messageId)
            redisClient.delete(key)
    redisClient.delete(pushKey)
    print('远端数据已清除')
