
from dotenv import load_dotenv

from gui import *


def gui_start():
    root = Tk()  # 实例化出一个父窗口
    LIVE_GUI = GUI(root)
    # 设置根窗口默认属性
    LIVE_GUI.setMainWindow()
    print(LIVE_GUI.liveId)
    root.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    load_dotenv()
    gui_start()
