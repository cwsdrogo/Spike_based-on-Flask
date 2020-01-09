
## 基于Flask的秒杀系统（简洁版）

####app.py  主程序
####config.py 配置文件
####exts.py 实例化MySQL和Redis连接
####models.py Sqlachemy

## 主程序包含了MySQL和redis的两种接口
## Redis基于watch实现的乐观锁是防止超卖的关键
### seckill 需要手动在redis-server设置初始值