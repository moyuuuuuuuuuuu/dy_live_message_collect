#!/usr/bin/.env python
# -*- coding: utf-8 -*-
from tkinter import Frame, Button, Tk, LEFT, RIGHT, Toplevel, Label, Entry, StringVar, Text, messagebox
import math
from component.DataList import DataList
from component.MessageFrame import MessageFrame
from component.InputGoodsWindow import InputGoodsWindow
from component.InputLiveWindow import InputLiveWindow

LOG_LINE_NUM = 0


class MainWindow(Tk):
    liveId = ''
    pageBarFrame = None
    mainWidth = 0
    mainHeight = 0
    spidering = False

    def __init__(self):
        super().__init__()

        self.inputWindow = None
        self.screenWidth, self.screenHeight = self.winfo_screenwidth(), self.winfo_screenheight()
        self.mainWidth, self.mainHeight = math.ceil(self.screenWidth / 2), math.ceil(self.screenHeight / 2)

        self.setMainWindow()
        self.setMainMenu()
        self.setMenuFrame()
        self.initTable()

    def setMainWindow(self):
        self.title("抖音直播弹幕采集")
        self.geometry('%dx%d+%d+%d' % (self.mainWidth, self.mainHeight, (self.screenWidth - self.mainWidth) // 2,
                                       (self.screenHeight - self.mainHeight) // 2))
        self.protocol('WM_DELETE_WINDOW', self.closeRoot)

    def setMainMenu(self):
        pass
        # menuBar = Menu(self)
        # # 创建文件的联级菜单
        # menu = Menu(menuBar, tearoff=0)
        # menu.add_command(label='直播间列表', accelerator='Ctrl+N')
        # menu.add_command(label='商品列表', accelerator='Ctrl+O')
        # menuBar.add_cascade(label='模式', menu=menu)
        # self['menu'] = menuBar

    def setMenuFrame(self):
        menuFrame = Frame(self, width=self.winfo_screenwidth(), height=40, padx=5, pady=5)
        menuFrame.pack(fill='x')

        createButton = Button(menuFrame, command=self.createLiveInputWindow, text='打开直播间')
        createButton.pack(side=LEFT)

        createButton = Button(menuFrame, command=self.createGoodsInputWindow, text='导入商品信息')
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

    def createGoodsInputWindow(self):
        self.inputGoodsWindow = InputGoodsWindow(self)
        self.inputGoodsWindow.show()

    def createLiveInputWindow(self):
        if self.inputWindow:
            messagebox.showinfo('提示', '正在采集，请勿重复操作')
            return
        self.inputWindow = InputLiveWindow(self, padx=5, pady=5)
        self.inputWindow.show()
        return

    def createListenLiveWindow(self):
        self.inputWindow.destroy()

        # self.spider.visit()
        # visitChrome(self.liveId)
