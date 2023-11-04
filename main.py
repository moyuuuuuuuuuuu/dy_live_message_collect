from dotenv import load_dotenv
from gui import *
from util.MysqlClient import MysqlClient
from util.Exporter import Exporter


def gui_start():
    LIVE_GUI = GUI()
    LIVE_GUI.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    load_dotenv()
    # gui_start()
    count = MysqlClient.count('live')
    limit = 100
    maxPage = int(count / limit) + 1
    print(maxPage)
    start = 1
    export = Exporter('test', ['id', '直播间ID', '发弹幕人数', '抓取时间'])

    for start in range(maxPage):
        list = MysqlClient.select(tablename='live', field='id,live_id,number,created_at', start=start + 1, limit=limit,
                                  order='number desc')
        # , start=(start - 1) * limit
        export.append(data=list)
    export.save()
