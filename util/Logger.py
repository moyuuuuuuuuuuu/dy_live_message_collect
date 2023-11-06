import logging, hashlib, os
from util.Config import Config
from datetime import datetime


def getlogfile():
    nameStyle = Config.instance().get('LOG_FILENAME_FORMAT')
    if nameStyle == 'date':
        filename = datetime.now().strftime("%Y-%m-%d")
    elif nameStyle == 'hash':
        filename = hashlib.md5(datetime.now().strftime("%Y-%m-%d"))
    else:
        filename = 'app'
    file = "{}{}.log".format(Config.instance().get('log_file_dir'), filename)
    if not os.path.exists(file):
        with open(file, 'w') as f:
            f.write(datetime.now().strftime("%Y-%m-%d"))
            f.close()

    return file


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    filename=getlogfile()
)

logger = logging.getLogger(__name__)
