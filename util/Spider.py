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
from util.Pool import getRedisConn

from tkinter import Toplevel, Label


class Spider():
    def __init__(self, master: Toplevel, liveId='', userDictFile=''):
        self.liveId = liveId
        self.userDictFile = userDictFile
        self.master = master

    def start(self, liveId=''):
        if not liveId:
            liveId = self.liveId
        pageUrl = "https://live.douyin.com/{}".format(liveId)
        self.master.focus_force()
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
                    redisConn = getRedisConn()
                    try:
                        es = ele.find_element(By.CLASS_NAME, 'webcast-chatroom___content-with-emoji-text')
                        id = ele.get_attribute('data-id')
                        hashKey = 'dy:message:hash:{}:{}'.format(liveId, id)
                        if not es or redisConn.exists(hashKey):
                            continue
                        pushKey = 'dy:message:push:{}'.format(liveId)
                        redisConn.lpush(pushKey, id)
                        redisConn.hset(hashKey, 'id', id)
                        redisConn.hset(hashKey, 'content', es.text)
                        redisConn.hset(hashKey, 'time', int(time.time()))
                        print("%s-%s-%s" % (
                            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            ele.get_attribute('data-id'),
                            es.text))
                        textComponent = Label(self.master, text="%s-%s-%s" % (
                            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            ele.get_attribute('data-id'),
                            es.text))
                        textComponent.pack(fill='x')
                        # 分词检测
                        self.master.update()
                    except NoSuchElementException:
                        pass
                    except StaleElementReferenceException:
                        pass
