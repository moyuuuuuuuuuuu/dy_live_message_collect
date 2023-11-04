from tkinter import Toplevel, Button, messagebox


class MessageFrame(Toplevel):
    liveId = None

    def __int__(self, master=None, cnf={}, **kw):
        Toplevel.__init__(master=master, cnf=cnf, **kw)
        self.root = master
        Button(master=self, text='采集结束', command=self.close).pack()

    def start(self, liveId):
        from util.Spider import Spider
        self.liveId = liveId
        self.spider = Spider(master=self, liveId=liveId)
        # self.spider.visit()

    def close(self):
        if messagebox.askokcancel('关闭', '确定关闭？'):
            self.destroy()
