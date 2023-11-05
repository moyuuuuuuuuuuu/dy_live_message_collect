import os
from util.Pool import getSqliteConn
from util.Config import Config


class Install:
    def install(self):
        """
        install_dir=INSTALL_DIR,
        sqlite_dir=SQLITE_DIR,
        sqlite_db=SQLITE_DB,
        lock_file_dir=LOCK_FILE_DIR,
        lock_file=LOCK_FILE,
        install_sql=
        :return:
        """
        if not os.path.exists(Config.instance().get('install_dir')):
            os.makedirs(Config.instance().get('install_dir'))

        if not os.path.exists(Config.instance().get('sqlite_dir')):
            os.makedirs(Config.instance().get('sqlite_dir'))

        if not os.path.exists(Config.instance().get('lock_file_dir')):
            os.makedirs(Config.instance().get('lock_file_dir'))

        if not os.path.exists(Config.instance().get('lock_file')):
            with open(Config.instance().get('lock_file'), 'w'):
                pass
        if not os.path.exists(Config.instance().get('sqlite_db')):
            with open(Config.instance().get('sqlite_db'), 'w'):
                pass

        connection = getSqliteConn()
        connection.execute(Config.instance().get('install_sql'))
        connection.close()
