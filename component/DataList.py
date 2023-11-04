import math
from tkinter import Frame, Menu, messagebox
from tkinter.ttk import Treeview
from util.MysqlClient import MysqlClient


class DataList(Frame):
    options = {
        'limit': 30,
        'maxPage': 0,
        'total': 0,
        'startPage': 1,
        'padding': (5, 10, 5, 10)
    }
    currentPage = 1
    listData = []
    pageBarFrame = None
    columns = []
    headers = []
    tablename = ''

    def __int__(self, master=None, cnf={}, **kw):
        Frame.__init__(master=master, cnf=cnf, **kw)
        self.root = master

    def setConfigure(self, **kwargs):
        self.options.update(kwargs)

    def initTable(self, tablename='', columns=[], headers=[], replacements={}, tags={}):
        self.columns = columns
        self.headers = headers
        self.tablename = tablename
        self.replacements = replacements
        self.table = Treeview(self, columns=columns, show='headings', height=self.options['limit'],
                              padding=self.options['padding'])
        self.table.pack(fill='x', expand=True)
        self.setTableHeader(columns=columns, headers=headers)
        self.table.bind('<Button-3>', self.opearMenu)
        self.initMenu()
        self.initTags(tags=tags)

    def initTags(self, tags={}):
        for tag in tags:
            self.table.tag_configure(tag, **tags[tag])

    def opearMenu(self, event):
        self.selectedItemEq = self.table.identify_row(event.y)
        # 获取当前行的数据
        self.item = self.table.item(self.selectedItemEq)
        self.table.menu.post(event.x_root, event.y_root)

    def initMenu(self):
        menu = Menu(self.table, tearoff=0)
        commandList = [
            {'label': '导出Excel', 'command': lambda: self.exportItem()},
            {'label': '导出云图', 'command': lambda: self.exportWordItem()},
            {'label': '删除', 'command': lambda: self.deleteItem()},
        ]
        for command in commandList:
            menu.add_command(label=command['label'], command=command['command'])
        self.table.menu = menu

    def exportItem(self):
        pass

    def exportWordItem(self):
        print(self.item)

    def deleteItem(self):
        MysqlClient.deleteByPk(self.table, int(self.item['values'][0]))
        self.table.delete(self.selectedItemEq)
        items = self.table.get_children()
        for i, item in enumerate(items):
            self.table.item(item, tags=(str(i),))

    def setTableHeader(self, columns=[], headers=[]):
        columnsLen = len(columns)
        for i in range(columnsLen):
            width = 70
            if 'width' in headers[i]:
                width = headers[i]['width']

            if 'text' in headers[i]:
                text = headers[i]['text']
            else:
                text = columns[i]
            self.table.heading(columns[i], text=text)
            self.table.column(columns[i], width=width, anchor='center')

    def refresh(self):
        listData, total = self.dataList.values()
        if self.currentPage == self.options.get('startPage', 1):
            self.options.update({
                'total': total,
                'maxPage': math.ceil(total / self.options['limit'])
            })
        if self.table.get_children():
            self.table.delete(*self.table.get_children())
        for i, item in enumerate(listData):
            modifyItem = list(item)
            for key, value in self.replacements.items():
                modifyItem[key] = value['label'][item[key]]
            modified_tuple = tuple(modifyItem)
            if i % 2 == 0:
                self.table.insert('', 'end', values=modified_tuple)
            else:
                self.table.insert('', 'end', values=modified_tuple, tags=('odd',))

        if self.pageBarFrame:
            self.pageBarFrame.upgrade()
        elif self.options.get('openPagination', False):
            self.initPageBar()

    def loadData(self):
        if self.options.get('openPagination', False):
            self.dataList = MysqlClient.dataList(tablename=self.tablename, start=self.currentPage,
                                               limit=self.options['limit'])
        else:
            self.dataList = MysqlClient.all(tablename=self.tablename)
        return self

    def render(self):
        self.loadData().refresh()

    def prev(self):
        self.currentPage -= 1
        if self.currentPage < self.options.get('startPage', 1):
            self.currentPage = 1
        self.loadData().refresh()

    def next(self):
        self.currentPage += 1
        if self.currentPage > self.options.get('maxPage', 1):
            self.currentPage = self.options.get('maxPage', 1)
        self.loadData().refresh()

    def changePage(self, page=1):
        if page < self.options.get('startPage', 1) or page > self.options.get('maxPage', 1):
            messagebox.showinfo('提示', '当前页码超出范围')
            return

        self.currentPage = page
        self.loadData().refresh()

    def reload(self):
        # self.table.destroy()
        # self.initTable(columns=self.columns, headers=self.headers, tablename=self.tablename)
        self.currentPage = self.options.get('startPage', 1)
        self.loadData().refresh()

    def initPageBar(self):
        from component.PaginationBar import PaginationBar

        self.pageBarFrame = PaginationBar(self, width=self.winfo_width(), height=40, padx=5, pady=5,
                                          bg='#d2d2d2')
        self.pageBarFrame.pack(fill='x')
