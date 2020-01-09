

from exts import db



class Seckill(db.Model):
    __tablename__ = "Seckill"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    left = db.Column(db.Integer)

