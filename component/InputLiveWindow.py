from tkinter import Toplevel, Label, Text, Entry, Button


class InputLiveWindow(Toplevel):

    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)
        self.master = master
        self.title('直播间信息')

    def show(self):
        self.geometry(
            f"+%d+%d" % (
                (self.master.screenWidth - self.master.mainWidth / 4) // 2, (self.master.screenHeight - 40) / 2))

        Label(self, text='直播间ID:').grid(row=0, column=0, padx=(10, 0), pady=10)  # 0行0列
        Entry(self, width=20).grid(row=0, column=1, columnspan=5, padx=(0, 10), ipadx=60)  # 0行1列，跨2列
        Label(self, text='触发关键字:').grid(row=1, column=0, padx=(10, 0))
        Text(self, width=30, height=5).grid(row=1, column=1, columnspan=5, padx=(0, 10))
        Label(self, text='上传商品信息文件:').grid(row=2, column=0, padx=(0, 10), ipady=10)
        # , command=chooseFileDialog
        Button(self, text="选择文件:").grid(row=2, column=1, columnspan=2, padx=(0, 10), ipadx=60)
        Button(self, text="确定").grid(row=3, column=0, pady=10, ipadx=30)
        Button(self, text="取消").grid(row=3, column=3, ipadx=30)
