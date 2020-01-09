

from flask_sqlalchemy import SQLAlchemy
import redis



pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password='123456')
rcon = redis.Redis(connection_pool=pool)
db = SQLAlchemy()
