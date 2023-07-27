import math
import time
import datetime
import redis
import argparse
import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
# pool = redis.ConnectionPool(host='62.234.36.164', port=6300, db=0, password='Redis8520')

pool = redis.ConnectionPool(host='******', port=6379, db=0)

def getRedis():
    return redis.Redis(connection_pool=pool)

def export(liveId):
    print('开始导出...')

    redisClient = getRedis()
    pushKey = 'dy:message:push:' + liveId
    lenPush = redisClient.llen(pushKey)

    limit = 1000  # 每批写入的行数
    num_batches = math.ceil(lenPush / limit)  # 总批数
    writer = pd.ExcelWriter(liveId+'.xlsx', engine='xlsxwriter')  # 创建一个 E
    for i in range(num_batches):
        start = i * limit
        end = min((i + 1) * limit, lenPush)

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
    print('导出完毕')


def visitChrome(liveId='989786608822'):
    pageUrl = "https://live.douyin.com/" + liveId
    option = Options()
    option.add_argument("--headless")  # 给option对象添加无头参数
    excetureService = Service(executable_path="chromedriver.exe")
    web = Chrome(service=excetureService)
    web.maximize_window()  # 窗口最大化
    web.get(pageUrl)
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "启动了")
    time.sleep(10)
    while True:
        eles = web.find_elements(By.CLASS_NAME, 'webcast-chatroom___enter-done')

        if len(eles) == 0:
            continue

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

                print(ele.get_attribute('data-id'), es.text, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            except NoSuchElementException:
                pass
            except StaleElementReferenceException:
                pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='直播弹幕采集')
    print("欢迎使用抖音直播弹幕采集")
    mode = input("请键入模式(collect采集模式[c] export 导出模式[e]):")

    liveId = input("请键入直播间ID:")
    # 添加命令行参数
    # parser.add_argument('-l', '--live', dest='liveId', help='直播间id', nargs='?', const='')
    # parser.add_argument('-m', '--mode', dest='mode', help='模式切换 collect采集模式 export导出模式', nargs='?',const='collect')
    # args = parser.parse_args()
    # mode = args.mode
    # liveId = args.liveId
    if not mode:
        print('请选择使用模式(collect:采集模式,export导出模式)')
    elif not liveId:
        print('请输入直播间id(直播间链接中得数字部分)')
    elif mode == 'collect' or mode == 'c':
        print('当前为采集模式，即将开始采集。退出请按Ctrl+C')
        print('开始采集直播弹幕')
        visitChrome(liveId)
    elif mode == 'export' or mode == 'e':
        print('当前为导出模式，即将开始导出。退出请按Ctrl+C')
        export(liveId)


