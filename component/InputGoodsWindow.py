from tkinter import Toplevel, filedialog, Label, Button, messagebox
from util.Importer import Importer
from component.progress import Progress as progress
from model.Goods import Goods


class InputGoodsWindow(Toplevel):
    chooseButton = None
    goodsFile = None

    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)
        self.master = master
        self.title('导入商品')

    def chooseFile(self):
        self.goodsFile = filedialog.askopenfilename()
        self.chooseButton.config(text=self.goodsFile)
        self.focus_force()

    def submit(self):
        if not self.goodsFile:
            messagebox.showerror(title='错误', message='请先选择文件')
            self.focus_force()
        else:
            # 创建进度条窗口
            master = self.master
            goodsFile = self.goodsFile
            self.destroy()
            width = 300
            height = 100
            progressWindow = progress(geometry=
                                      f"%dx%d+%d+%d" % (
                                          width, height, (master.screenWidth - master.mainWidth / 4) // 2,
                                          (master.screenHeight - 40) / 2))

            importer = Importer()
            importer.load(goodsFile)
            goodsData = importer.toList()
            if goodsData and Goods().batchInsert(goodsData):
                progressWindow.close()
            master.focus_force()

    def show(self):
        self.geometry(
            f"+%d+%d" % (
                (self.master.screenWidth - self.master.mainWidth / 4) // 2, (self.master.screenHeight - 40) / 2))
        Label(self, text='上传商品信息文件:').grid(row=2, column=0, padx=(0, 10), ipady=10)
        self.chooseButton = Button(self, text="选择文件",
                                   command=self.chooseFile)
        self.chooseButton.grid(row=2, column=1, columnspan=2, padx=(0, 10), ipadx=60)
        Button(self, text="确定",
               command=self.submit).grid(row=3, column=0, pady=10, ipadx=30)
        Button(self, text="取消",
               command=self.destroy).grid(row=3, column=3, ipadx=30)
