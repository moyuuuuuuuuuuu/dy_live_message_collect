from dotenv import load_dotenv
from gui import *
from logic.Logic import Logic, getRedisClient
import json
from util.Pool import redisPool


def gui_start():
    LIVE_GUI = GUI()
    LIVE_GUI.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    load_dotenv()
    gui_start()

