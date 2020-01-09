from flask import Flask, jsonify
from models import Seckill
from exts import db, rcon
import config


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

#  push 上下文，首次运行需要创建表
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
            return jsonify('failed')
        return jsonify('success')
    return jsonify('failed')

@app.route('/Seckill_redis', methods=['POST'])
def seckill_redis():
    '''基于redis，超卖现象消失'''
    rcon.watch('seckill')
    left = rcon.get('seckill')
    if int(left.decode()) > 0:
        rcon.decr('seckill')
        return jsonify('success')
    return jsonify('failed')


if __name__ == '__main__':
    app.run()