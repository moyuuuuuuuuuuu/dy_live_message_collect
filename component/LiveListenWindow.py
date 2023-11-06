from threading import Thread
from tkinter import Toplevel, messagebox, Button
from tkinter.ttk import Treeview

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

        columns = ('时间', '弹幕id', '内容')
        self.treeview = Treeview(self, columns=columns, height=self.master.mainHeight // 20)
        self.treeview.pack(fill='x', expand=True)
        for i in range(len(columns)):
            self.treeview.heading(columns[i], text=columns[i])
            self.treeview.column(columns[i], anchor='center')
        # time.sleep()
        spider = Spider(master=self.treeview, liveId=liveId, userDictFile=userDictFile)
        self.thread = Thread(target=spider.start())
        self.thread.start()
        self.thread.join()

    def warning(self):
        if messagebox.showinfo('提示', '直播已经结束'):
            self.spidering = False

    def close(self):
        if self.spidering:
            if not messagebox.askyesno('销毁？', '正在采集，确定要退出吗？'):
                return
        self.spidering = False
        if self.opera != 0:
            # TODO:保存数据到excel或者数据库
            pass
        self.destroy()
