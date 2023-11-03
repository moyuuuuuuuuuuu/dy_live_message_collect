#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import *
import hashlib
import math
from data import *
from component.DataList import DataList
from tkinter import messagebox
from component.MessageFrame import MessageFrame

LOG_LINE_NUM = 0


class GUI(Tk):
    liveId = ''
    pageBarFrame = None
    mainWidth = 0
    mainHeight = 0
    spidering = False

    def __init__(self):
        super().__init__()

        self.screenWidth, self.screenHeight = self.winfo_screenwidth(), self.winfo_screenheight()
        self.mainWidth, self.mainHeight = math.ceil(self.screenWidth / 2), math.ceil(self.screenHeight / 2)

        self.data = Data()
        self.setMainWindow()
        self.setMenuFrame()
        self.initTable()

    def setMainWindow(self):
        self.title("抖音直播弹幕采集")
        self.geometry('%dx%d' % (self.mainWidth, self.mainHeight))
        self.protocol('WM_DELETE_WINDOW', self.closeRoot)

    def setMenuFrame(self):
        menuFrame = Frame(self, width=self.winfo_screenwidth(), height=40, padx=5, pady=5)
        menuFrame.pack(fill='x')

        createButton = Button(menuFrame, command=self.createNewliveWindow, text='打开直播间')
        createButton.pack(side=LEFT)

        refreshButton = Button(menuFrame, command=self.refreshTable, text='刷新')
        refreshButton.pack(side=RIGHT)

    def closeRoot(self):
        # if messagebox.askokcancel("退出?", "确定退出吗?"):
        self.quit()

    def initTable(self):
        columns = ('ID', '直播间ID', '采集时间', '弹幕数量', '是否导出excel', '是否导出词云')
        headers = [
            {
                'text': 'ID',
                'width': 80
            },
            {
                'text': '直播间ID',
                'width': 80
            },
            {
                'text': '采集时间',
                'width': 120
            },
            {
                'text': '弹幕数量',
            },
            {
                'text': '是否导出excel',

            },
            {
                'text': '是否导出词云',
            }
        ]
        replacements = {
            4: {
                'label': ['未导出', '已导出'],
            },
            5: {
                'label': ['未导出', '已导出'],
            }
        }
        self.tableFrame = DataList(self, width=self.mainWidth, height=self.mainHeight)
        self.tableFrame.pack(fill='x')
        self.tableFrame.setConfigure({'openPagination': True})
        self.tableFrame.initTable(columns=columns, headers=headers, replacements=replacements, tablename='live')
        self.tableFrame.start()

    def refreshTable(self):
        self.tableFrame.reload()

    def listenEntryChange(self, entryText):
        self.liveId = entryText.get()

    def createNewliveWindow(self):
        if self.spidering:
            messagebox.showinfo('提示', '正在采集，请勿重复操作')
            # self.createNewliveWindow()
        self.inputWindow = Toplevel(self, padx=5, pady=5)
        self.inputWindow.geometry('%dx%d' % (self.mainWidth / 3, self.mainHeight / 3))
        self.inputWindow.protocol('WM_DELETE_WINDOW', self.closeInputWindow)
        self.inputWindow.pack_slaves()
        Label(self.inputWindow, text='请输入直播间id:').grid(column=2, row=2)
        entryText = StringVar()
        entryText.trace('w', lambda name, index, mode, entryText=entryText: self.listenEntryChange(entryText))
        Entry(self.inputWindow, bd=1, textvariable=entryText).grid(column=4, row=2)
        Button(self.inputWindow, text='确定', command=self.createBeginListenLiveWindow).grid(column=6, row=2)

    def closeInputWindow(self):
        self.liveId = ''
        self.inputWindow.destroy()
        print(self.liveId)

    def createBeginListenLiveWindow(self):
        self.inputWindow.destroy()
        # 创建一个ListBox窗口
        self.liveId = '44304010917'
        print(self.liveId)
        self.spidering = True
        self.messageFrame = MessageFrame(self)

        self.messageFrame.geometry('%dx%d' % (self.mainWidth, self.mainHeight))
        self.messageFrame.title = '直播间弹幕采集'
        self.messageFrame.protocol('WM_DELETE_WINDOW', self.messageFrame.close)
        # 更新主页面
        self.update()
        self.messageFrame.pack_slaves()
        self.messageFrame.start(liveId=self.liveId)
        # self.spider.visit()
        # visitChrome(self.liveId)


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
