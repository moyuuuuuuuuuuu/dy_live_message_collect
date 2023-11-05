#! /usr/bin/python
# -*- coding: utf-8 -*-

from dotenv import load_dotenv
from component.MainWindow import *
from util.Importer import *
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from logic.Install import Install
from util.Config import Config


def app():
    root = Tk()  # 源码来自wb98.com

    la1 = Label(root, text='直播间ID：')
    la1.grid(row=0, column=0, padx=(10, 0), pady=10)  # 0行0列

    en1 = Entry(root, width=30)  # 用户名文本框
    en1.grid(row=0, column=1, columnspan=5, padx=(0, 10), ipadx=60)  # 0行1列，跨2列

    la2 = Label(root, text='触发关键字：')
    la2.grid(row=1, column=0, padx=(10, 0))

    en2 = Text(root, width=30, height=5)  # 密码文本框
    en2.grid(row=1, column=1, columnspan=5, padx=(0, 10), ipadx=60)  # 1行1列，跨2列

    la2 = Label(root, text='上传商品信息文件：')
    la2.grid(row=2, column=0, padx=(0, 10), ipady=10)

    Button(root, text="选择文件", command=chooseFileDialog).grid(row=2, column=1, columnspan=2, padx=(0, 10), ipadx=60)

    but1 = Button(root, text="确定")
    but1.grid(row=3, column=0, pady=10, ipadx=30)
    but2 = Button(root, text="取消")
    but2.grid(row=3, column=3, ipadx=30)

    root.mainloop()


def chooseFileDialog():
    file_path = filedialog.askopenfilename()


def readExcel():
    file = "C:/Users/janma/Desktop/商品信息.xlsx"
    importer = Importer()
    importer.load(file_path=file)
    productMap = importer.toList()
    columns = importer.getColumns()

    print(productMap, columns)


Install_SQL = '''
CREATE TABLE IF NOT EXISTS goods (
    id INTEGER PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    keyword VARCHAR(50) NOT NULL ,
    stock INT
    price DECIMAL(10,2)
)
'''


def root():
    masterWindow = MainWindow()
    masterWindow.mainloop()

def start_progress(progress_bar):
    progress_bar.start()


def stop_progress(progress_bar):
    progress_bar.stop()


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    load_dotenv()

    INSTALL_DIR = os.path.expanduser('~') + os.getenv('INSTALL_PATH')
    SQLITE_DIR = INSTALL_DIR + os.getenv('SQLITE_DIR')
    SQLITE_DB_NAME = os.getenv('SQLITE_DB')
    SQLITE_DB = SQLITE_DIR + SQLITE_DB_NAME + '.db'
    LOCK_FILE_DIR = INSTALL_DIR + os.getenv('LOCK_FILE_DIR')
    LOCK_FILE = LOCK_FILE_DIR + os.getenv('LOCK_FILE')
    INSTALL_SQL_FILE = INSTALL_DIR + os.getenv('INSTALL_SQL_FILE')
    Config.instance().setConfig(
        install_dir=INSTALL_DIR,
        sqlite_dir=SQLITE_DIR,
        sqlite_db=SQLITE_DB,
        sqlite_db_name=SQLITE_DB_NAME,
        lock_file_dir=LOCK_FILE_DIR,
        lock_file=LOCK_FILE,
        install_sql=Install_SQL
    )

    # 检测是否安装
    if not os.path.exists(LOCK_FILE):
        Install().install()
    # app()

    root()
    # readExcel()
    # sqliteConn = getSqliteConn('test')
    # sqliteConn.execute(initSQL)
    # where = [('id', '<>', 123), ('name', 'like', '%张%'), ('BETWEEN', 'name', '1', '3'), 'FIND_IN_SET("a",123)',
    #          {"id": 111}]
    # whereString, whereArgs = buildWhere(where)
    #
    # print(whereString, (whereArgs))
