#!/usr/bin/.env python
# -*- coding: utf-8 -*-
from tkinter import Frame,Button,Tk,LEFT,RIGHT
import math
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

        self.setMainWindow()
        self.setMenuFrame()
        self.initTable()

    def setMainWindow(self):
        self.title("抖音直播弹幕采集")
        self.geometry('%dx%d+%d+%d' % (self.mainWidth, self.mainHeight, (self.screenWidth - self.mainWidth) // 2,
                                       (self.screenHeight - self.mainHeight) // 2))
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
        self.tableFrame = DataList(self, width=self.mainWidth, height=(self.mainHeight - 120))
        self.tableFrame.pack(fill='x')
        self.tableFrame.setConfigure(
            openPagination=True,
            limit=(self.mainHeight - 120) // 20,
        )
        self.tableFrame.initTable(
            tablename='live',
            columns=columns,
            headers=headers,
            replacements=replacements,
            tags={
                "odd": {
                    "background": "#f0f0f0"
                },
            }
        )
        self.tableFrame.render()

    def refreshTable(self):
        self.tableFrame.reload()

    def listenEntryChange(self, entryText):
        self.liveId = entryText.get()

    def createNewliveWindow(self):
        if self.spidering:
            messagebox.showinfo('提示', '正在采集，请勿重复操作')
            return
            # self.createNewliveWindow()
        self.inputWindow = Toplevel(self, padx=5, pady=5)
        self.inputWindow.geometry(
            f"%dx%d+%d+%d" % (
                max(self.mainWidth / 4, 300), 40, (self.screenWidth - self.mainWidth / 4) // 2,
                (self.screenHeight - 40) / 2))
        self.inputWindow.protocol('WM_DELETE_WINDOW', self.closeInputWindow)
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
        self.messageFrame.title = '直播间弹幕采集'
        self.messageFrame.geometry(
            '%dx%d+%d+%d' % (self.mainWidth, self.mainHeight, (self.screenWidth - self.mainWidth) // 2 + 30,
                             (self.screenHeight - self.mainHeight) // 2 + 30))
        self.messageFrame.protocol('WM_DELETE_WINDOW', self.messageFrame.close)
        # self.messageFrame.grab_set()
        # 更新主页面
        self.messageFrame.pack_slaves()
        self.messageFrame.start(liveId=self.liveId)
        self.update()
        # self.spider.visit()
        # visitChrome(self.liveId)
