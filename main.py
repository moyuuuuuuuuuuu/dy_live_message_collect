#! /usr/bin/python
# -*- coding: utf-8 -*-

from dotenv import load_dotenv

from component.MainWindow import *
from logic.Install import Install
from util.Config import Config
from util.Importer import *
from util.MysqlClient import MysqlClient

Install_SQL = '''
CREATE TABLE IF NOT EXISTS goods (
    id INTEGER PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    weight VARCHAR(50) NOT NULL ,
    g INT NOT NULL DEFAULT 0 ,
    price DECIMAL(10,2),
    remark VARCHAR(150) NOT NULL DEFAULT ''
)
'''


def root():
    masterWindow = MainWindow()
    masterWindow.mainloop()


def registerConfig():
    INSTALL_DIR = os.path.expanduser('~') + os.getenv('INSTALL_PATH')
    SQLITE_DIR = INSTALL_DIR + os.getenv('SQLITE_DIR')
    SQLITE_DB_NAME = os.getenv('SQLITE_DB')
    SQLITE_DB = SQLITE_DIR + SQLITE_DB_NAME + '.db'
    LOCK_FILE_DIR = INSTALL_DIR + os.getenv('LOCK_FILE_DIR')
    LOCK_FILE = LOCK_FILE_DIR + os.getenv('LOCK_FILE')
    LOG_FILE_DIR = INSTALL_DIR + os.getenv('LOG_FILE_DIR')
    LOG_FILENAME_FORMAT = LOG_FILE_DIR + os.getenv('LOG_FILENAME_FORMAT')
    Config.instance().setConfig(
        install_dir=INSTALL_DIR,
        sqlite_dir=SQLITE_DIR,
        sqlite_db=SQLITE_DB,
        sqlite_db_name=SQLITE_DB_NAME,
        lock_file_dir=LOCK_FILE_DIR,
        lock_file=LOCK_FILE,
        install_sql=Install_SQL,
        log_file_dir=LOG_FILE_DIR,
        LOG_FILENAME_FORMAT=LOG_FILENAME_FORMAT
    )


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    load_dotenv()
    registerConfig()
    Install().installChk()
    root()
