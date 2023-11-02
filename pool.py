import os
from dotenv import load_dotenv
import redis
pool = redis.ConnectionPool(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=os.getenv('REDIS_DB'),
                            password=os.getenv('REDIS_PASSWORD'))