from tkinter import LEFT, RIGHT, Button, Frame
from component.DataList import DataList


class PaginationBar(Frame):
    buttonWidth = 5
    buttonNumber = 12
    pageBarButtonList = []

    def __init__(self, master: DataList, cnf={}, **kw):
        super().__init__(master=master, cnf=cnf, **kw)
        self.root = master
        self.initPageBar()

    def initPageBar(self):
        # 首页按钮
        firstBar = Button(self, text='首页', command=lambda: self.root.changePage(1), width=self.buttonWidth,
                          foreground='#ff422e', background='#ffffff', font=('Arial', 12, 'bold'))
        firstBar.pack(side=LEFT)

        # 尾页按钮
        endBar = Button(self, text='尾页', command=lambda: self.root.changePage(self.root.options.get('maxPage')),
                        width=self.buttonWidth,
                        foreground='#ff422e', background='#ffffff', font=('Arial', 12, 'bold'))
        endBar.pack(side=RIGHT)
        # 上一页
        prevBar = Button(self, text='< Prev', command=self.root.prev, width=self.buttonWidth,
                         foreground='#ff422e', background='#ffffff', font=('Arial', 12, 'bold'))
        prevBar.pack(side=LEFT)
        # 下一页
        nextBar = Button(self, text='Next >', command=self.root.next, width=self.buttonWidth,
                         foreground='#ff422e', background='#ffffff', font=('Arial', 12, 'bold'))
        nextBar.pack(side=RIGHT)

        self.renderPageBar()

    def renderPageBar(self):
        btnNumber = self.buttonNumber
        maxPage = self.root.options.get('maxPage', 1)
        minPage = self.root.options.get('startPage', 1)
        currentPage = self.root.currentPage

        if currentPage < minPage:
            startPage, endPage = minPage, minPage + btnNumber
        elif currentPage > maxPage:
            startPage, endPage = maxPage - btnNumber, maxPage
        elif currentPage + btnNumber > maxPage:
            startPage, endPage = maxPage - btnNumber + 1, maxPage + 1
        else:
            startPage, endPage = currentPage, currentPage + btnNumber

        print(self.root.currentPage, minPage, maxPage, startPage, endPage)
        for i in range(startPage, endPage):
            if i == currentPage:
                pageBar = Button(self, text=str(i), width=self.buttonWidth,
                                 foreground='#ffffff', background='#ff422e', font=('Arial', 12, 'bold'))
            else:
                pageBar = Button(self, text=str(i), width=self.buttonWidth, command=lambda: self.root.changePage(page=i),
                                 foreground='#ff422e', background='#ffffff', font=('Arial', 12, 'bold'))
            pageBar.pack(side=LEFT)
            self.pageBarButtonList.append(pageBar)

    def changePage(self, page):
        print(int(page))

    def nextPage(self):
        self.root.next()

    def prevPage(self):
        self.root.prev()

    def upgrade(self):
        for button in self.pageBarButtonList:
            button.destroy()
        self.renderPageBar()
