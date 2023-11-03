#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox
from tkinter.ttk import Treeview
import hashlib
from spider import *
from data import *

LOG_LINE_NUM = 0


class GUI(Tk):
    liveId = ''
    pageBarFrame = None

    def __init__(self):
        super().__init__()
        self.data = Data()
        self.setMainWindow()
        self.setMenuFrame()
        self.initTable()

    def setMainWindow(self):
        self.title("抖音直播弹幕采集")
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry('%dx%d' % (math.ceil(width / 2), math.ceil(height / 2)))
        self.protocol('WM_DELETE_WINDOW', self.closeRoot)

    def setMenuFrame(self):
        menuFrame = Frame(self, width=self.winfo_screenwidth(), height=40, padx=5, pady=5)
        menuFrame.pack(fill='x')

        createButton = Button(menuFrame, command=self.createNewliveWindow, text='打开直播间')
        createButton.pack(side=LEFT)

        refreshButton = Button(menuFrame, command=self.refreshTable, text='刷新')
        refreshButton.pack(side=RIGHT)

    def closeRoot(self):
        if messagebox.askokcancel("退出?", "确定退出吗?"):
            self.destroy()

    def initTable(self):
        columns = ('直播间ID', '采集时间', '弹幕数量')
        area = ('直播间ID', '采集时间', '弹幕数量')
        self.table = Treeview(self, columns=columns, show='headings', padding=(10, 10, 10, 10), height=10)
        self.table.pack(fill='x')

        # limitFilterMenuBar = Menu(self)
        # limitFilterMenu = Menu(limitFilterMenuBar, tearoff=0)
        # limitFilterMenu.add_command(label='每页50条', command=lambda: Data.changeLimit(50))
        # limitFilterMenu.add_command(label='每页100条', command=lambda: Data.changeLimit(100))
        # limitFilterMenu.add_command(label='每页500条', command=lambda: Data.changeLimit(500))
        # limitFilterMenu.add_command(label='每页1000条', command=lambda: Data.changeLimit(1000))
        # limitFilterMenuBar.add_command(label='每页2000条', command=lambda: Data.changeLimit(2000))
        for i in range(3):
            self.table.column(columns[i], width=70, anchor='e')
            self.table.heading(columns[i], text=area[i])
        dataList = self.data.loadData(self.data.currentPage, self.data.limit)
        self.initPageBar()
        [list, count] = dataList.values()
        print(list)
        for item in list:
            self.table.insert('', 'end', values=item)
        # 计算页数

    def refreshTable(self):
        # 刷新表格
        self.data.refresh()
        # 刷新分页器
        self.initPageBar()

    def initPageBar(self):
        if self.pageBarFrame:
            self.pageBarFrame.destroy()

        self.pageBarFrame = Frame(self, width=self.winfo_screenwidth(), height=40, padx=5, pady=5, bg='#f3f3f3')
        self.pageBarFrame.pack(fill='x')
        # 按钮宽度
        buttonWidth = 5
        # 中间需要展示的翻页按钮数量
        btnNumber = 12
        # 初始页码计算
        [currentPage, minPage, maxPage] = [self.data.currentPage, 1, self.data.maxPage]
        # 首页按钮
        firstBar = Button(self.pageBarFrame, text='首页', command=lambda: self.changePage(1), width=buttonWidth,
                          foreground='#ff422e', background='#ffffff', font=('Arial', 12, 'bold'))
        firstBar.pack(side=LEFT)
        # 尾页按钮
        endBar = Button(self.pageBarFrame, text='尾页', command=lambda: self.changePage(maxPage), width=buttonWidth,
                        foreground='#ff422e', background='#ffffff', font=('Arial', 12, 'bold'))
        endBar.pack(side=RIGHT)
        # 上一页
        prevBar = Button(self.pageBarFrame, text='< Prev', command=self.prevPage, width=buttonWidth,
                         foreground='#ff422e', background='#ffffff', font=('Arial', 12, 'bold'))
        prevBar.pack(side=LEFT)
        # 下一页
        nextBar = Button(self.pageBarFrame, text='Next >', command=self.nextPage, width=buttonWidth,
                         foreground='#ff422e', background='#ffffff', font=('Arial', 12, 'bold'))
        nextBar.pack(side=RIGHT)

        if currentPage < minPage:
            startPage = minPage
            endPage = minPage + btnNumber
        elif currentPage > maxPage:
            startPage = maxPage - btnNumber
            endPage = maxPage
        elif currentPage + btnNumber > maxPage:
            startPage = maxPage - btnNumber + 1
            endPage = maxPage + 1
        else:
            startPage = currentPage
            endPage = currentPage + btnNumber

        print(startPage, endPage, "当前页%d" % currentPage,
              "最小%d" % minPage, "最大%d" % maxPage, "按钮数量%d" % btnNumber)
        for i in range(startPage, endPage):
            if i == currentPage:
                pageBar = Button(self.pageBarFrame, text=str(i), width=buttonWidth,
                                 foreground='#ffffff', background='#ff422e', font=('Arial', 12, 'bold'))
            else:
                pageBar = Button(self.pageBarFrame, text=str(i), width=buttonWidth, command=lambda: self.changePage(i),
                                 foreground='#ff422e', background='#ffffff', font=('Arial', 12, 'bold'))

            pageBar.pack(side=LEFT)

    def changePage(self, page):
        print(page)
        self.data.page(page=page)
        self.initPageBar()

    def nextPage(self):
        self.data.next()
        self.initPageBar()

    def prevPage(self):
        self.data.prev()
        self.initPageBar()

    def listenEntryChange(self, entryText):
        self.liveId = entryText.get()

    def createNewliveWindow(self):
        print('创建监听直播间窗口')
        # self.inputWindow = tkinter.Toplevel(self.root)
        # self.inputWindow.protocol('WM_DELETE_WINDOW', self.closeInputWindow)
        # self.inputWindow.grid()
        # label = Label(self.inputWindow, text='请输入直播间id')
        # label.pack()
        # entryText = StringVar()
        # entryText.trace('w', lambda name, index, mode, entryText=entryText: self.listenEntryChange(entryText))
        # input = Entry(self.inputWindow, bd=1, textvariable=entryText)
        # input.pack()
        # submit = Button(self.inputWindow, text='确定', command=self.createBeginListenLiveWindow)
        # submit.propagate
        # submit.pack()

    def closeInputWindow(self):
        self.liveId = ''
        self.inputWindow.destroy()
        print(self.liveId)

    def createBeginListenLiveWindow(self):
        print('抓取弹幕')
        self.inputWindow.destroy()
        # 创建一个ListBox窗口
        visitChrome(self.liveId)


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
