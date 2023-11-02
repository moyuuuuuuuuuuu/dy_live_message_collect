#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter
from tkinter import *
from tkinter import ttk
import hashlib
from spider import *
LOG_LINE_NUM = 0


class GUI():
    liveId = ''

    def __init__(self, root):
        self.root = root
        self.screenWidth = self.root.winfo_screenwidth()
        self.screenHeight = self.root.winfo_screenheight()

    def listenEntryChange(self, entryText):
        self.liveId = entryText.get()

    def createNewliveWindow(self):
        print('创建监听直播间窗口')
        self.inputWindow = tkinter.Toplevel(self.root)
        self.inputWindow.protocol('WM_DELETE_WINDOW', self.closeInputWindow)
        self.inputWindow.grid()
        label = Label(self.inputWindow, text='请输入直播间id')
        label.pack()
        entryText = StringVar()
        entryText.trace('w', lambda name, index, mode, entryText=entryText: self.listenEntryChange(entryText))
        input = Entry(self.inputWindow, bd=1, textvariable=entryText)
        input.pack()
        submit = Button(self.inputWindow, text='确定', command=self.createBeginListenLiveWindow)
        submit.propagate
        submit.pack()

    def closeInputWindow(self):
        self.liveId = ''
        self.inputWindow.destroy()
        print(self.liveId)

    def createBeginListenLiveWindow(self):
        print('抓取弹幕')
        self.inputWindow.destroy()
        #创建一个ListBox窗口
        visitChrome(self.liveId)

    def setMainWindow(self):
        # 初始化主页面
        self.root.title("抖音直播弹幕采集")
        self.mainWindow = Frame(self.root, width=math.ceil(self.screenWidth / 2),
                                height=math.ceil(self.screenHeight / 2))
        self.mainWindow.pack(fill=BOTH, expand=True)
        self.initTable()

    def initTable(self):
        columns = ('直播间ID', '采集时间', '弹幕数量')
        area = ('直播间ID', '采集时间', '弹幕数量')
        self.table = ttk.Treeview(self.mainWindow, columns=columns, show='headings', padding=(10, 5, 20, 30))
        self.table.button = Button(self.mainWindow, text='创建新直播', command=self.createNewliveWindow)
        self.table.button.pack()
        data = [
            (1231231213, '2011-11-11', 600),
            (2342342343, '2011-11-11', 600),
            (45645645, '2011-11-11', 600),
            (67867867, '2011-11-11', 600),
            (456789, '2011-11-11', 600),
        ]

        for i in range(3):
            self.table.column(columns[i], width=70, anchor='e')
            self.table.heading(columns[i], text=area[i])

        self.table.pack()
        # print()
        dataLength = int(len(data))
        for item in data:
            self.table.insert('', 'end', values=item)

        def select(*args):
            print(self.table.bbox(self.table.selection()))
            print(self.table.bbox(self.table.selection(), column='c'))

        self.table.bind('<<TreeviewSelect>>', select)


class MY_GUI():
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name

    # 设置窗口
    def set_init_window(self):
        self.init_window_name.title("文本处理工具_v1.2")  # 窗口名
        # self.init_window_name.geometry('320x160+10+10')                         #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name.geometry('1068x681+10+10')
        # self.init_window_name["bg"] = "pink"                                    #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        # self.init_window_name.attributes("-alpha",0.9)                          #虚化，值越小虚化程度越高
        # 标签
        self.init_data_label = Label(self.init_window_name, text="待处理数据")
        self.init_data_label.grid(row=0, column=0)
        self.result_data_label = Label(self.init_window_name, text="输出结果")
        self.result_data_label.grid(row=0, column=12)
        self.log_label = Label(self.init_window_name, text="日志")
        self.log_label.grid(row=12, column=0)
        # 文本框
        self.init_data_Text = Text(self.init_window_name, width=67, height=35)  # 原始数据录入框
        self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)
        self.result_data_Text = Text(self.init_window_name, width=70, height=49)  # 处理结果展示
        self.result_data_Text.grid(row=1, column=12, rowspan=15, columnspan=10)
        self.log_data_Text = Text(self.init_window_name, width=66, height=9)  # 日志框
        self.log_data_Text.grid(row=13, column=0, columnspan=10)
        # 按钮
        self.str_trans_to_md5_button = Button(self.init_window_name, text="字符串转MD5", bg="lightblue", width=10,
                                              command=self.str_trans_to_md5)  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.grid(row=1, column=11)

    # 功能函数
    def str_trans_to_md5(self):
        src = self.init_data_Text.get(1.0, END).strip().replace("\n", "").encode()
        # print("src =",src)
        if src:
            try:
                myMd5 = hashlib.md5()
                myMd5.update(src)
                myMd5_Digest = myMd5.hexdigest()
                # print(myMd5_Digest)
                # 输出到界面
                self.result_data_Text.delete(1.0, END)
                self.result_data_Text.insert(1.0, myMd5_Digest)
                self.write_log_to_Text("INFO:str_trans_to_md5 success")
            except:
                self.result_data_Text.delete(1.0, END)
                self.result_data_Text.insert(1.0, "字符串转MD5失败")
        else:
            self.write_log_to_Text("ERROR:str_trans_to_md5 failed")

    # 获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return current_time

    # 日志动态打印
    def write_log_to_Text(self, logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) + " " + str(logmsg) + "\n"  # 换行
        if LOG_LINE_NUM <= 7:
            self.log_data_Text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_Text.delete(1.0, 2.0)
            self.log_data_Text.insert(END, logmsg_in)
