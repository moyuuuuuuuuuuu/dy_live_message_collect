import os
import redis
from dotenv import load_dotenv
from mysql.connector.pooling import MySQLConnectionPool

load_dotenv()
mysqlPool = MySQLConnectionPool(
    host=str(os.getenv('MYSQL_HOST')),  # 数据库主机地址
    user=str(os.getenv('MYSQL_USER')),  # 数据库用户名
    passwd=str(os.getenv('MYSQL_PASSWORD')),  # 数据库密码
    port=int(os.getenv('MYSQL_PORT')),
    database=str(os.getenv('MYSQL_DB')),
    pool_size=int(os.getenv('MYSQL_POOL_SIZE')),
)
redisPool = redis.ConnectionPool(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=os.getenv('REDIS_DB'),
                                 password=os.getenv('REDIS_PASSWORD'))
