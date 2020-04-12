from flask import Flask, jsonify
from models import Seckill
from exts import db, rcon
from redis import WatchError
import config


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

#  push 上下文，首次运行需要创建表。但需要手动创建数据库
#  也可以使用 app.before_first_request 来装饰一个函数
# with app.app_context():
#     db.create_all()


@app.route('/Seckill', methods=['POST'])
def seckill():
    '''基于MySQL，100个会有几个超卖的现象'''
    goods = Seckill.query.filter(Seckill.left > 0).first()
    if goods and goods.left:
        goods.left -= 1
        try:
            db.session.add(goods)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify('interrupt failed')
        return jsonify('success')
    return jsonify('failed')

@app.route('/Seckill_redis', methods=['POST'])
def seckill_redis():
    '''基于redis，超卖现象消失'''
    pipe = rcon.pipeline()
    pipe.watch('seckill')  #  rcon.watch 不能配合事务奏效
    left = rcon.get('seckill')
    # rcon.set('seckill', 11)  #  watch 和 multi 之间也能触发乐观锁
    if int(left) > 0:
        #  开启事务
        pipe.multi()
        pipe.decr('seckill')
        try:
            pipe.execute()
            return jsonify('success')
        except WatchError as e:
            print(e)  #  Watched variable changed.
        return jsonify('interrupt failed')
    return jsonify('failed')


if __name__ == '__main__':
    app.run()