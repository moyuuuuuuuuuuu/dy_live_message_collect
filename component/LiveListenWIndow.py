from tkinter import Toplevel, messagebox, Button
from util.Spider import Spider


class LiveListenWindow(Toplevel):
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)
        self.master = master
        # 324980718774
        self.geometry('%dx%d+%d+%d' % (
            master.mainWidth, master.mainHeight, (master.screenWidth - master.mainWidth) // 2 + 30,
            (master.screenHeight - master.mainHeight) // 2 + 30))
        self.title('直播间弹幕采集')
        self.focus_force()
        Button(self, text='采集结束', command=self.close).pack()

    def show(self, liveId='', userDictFile='', opera=0):
        self.liveId = liveId
        self.spidering = True
        self.opera = opera
        self.protocol('WM_DELETE_WINDOW', self.close)
        # 唤醒Spider 并把参数传给它
        Spider(master=self, liveId=liveId, userDictFile=userDictFile).start()
        pass

    def close(self):
        if self.spidering:
            if not messagebox.askquestion('销毁？', '正在采集，确定要退出吗？'):
                return
        if self.opera != 0:
            # TODO:保存数据到excel或者数据库
            pass
        self.destroy()
