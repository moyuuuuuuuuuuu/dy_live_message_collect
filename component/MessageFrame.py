from tkinter import Toplevel, messagebox, Frame


class MessageFrame(Frame):
    liveId = None

    def __int__(self, master=None, cnf={}, **kw):
        Toplevel.__init__(master=master, cnf=cnf, **kw)
        self.root = master

    def start(self, liveId):
        pass

    def close(self):
        if messagebox.askokcancel('关闭', '确定关闭？'):
            self.destroy()
