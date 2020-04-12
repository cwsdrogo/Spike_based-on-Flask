import requests
import threading
import time
from exts import rcon

'''
    间隔两秒进行测试
    如果有超卖现象，会将时间和超卖量记录到log.txt
    即使tn > left ，最后也会存在库存量 > 0的情况
        原因是乐观锁的机制，导致已经进入事务的线程没能修改成功，并且该次机会浪费了
    即使某个线程在 watch 和 multi 之间的代码执行时，另一个线程修改了库存，也是能触发乐观锁的
'''

tn = 50  #  同时开启的线程数
left = 40 #  库存量
verbose = 0

url = 'http://127.0.0.1:5000/Seckill_redis'


def update_views():
    '''超时会重发请求'''
    flag = 1
    while flag:
        try:
            resp = requests.post(url)
            if verbose:
                print(resp.text)
            flag = 0
        #  并发下，超过负载的部分用户请求延时重发。代价是响应时间过长
        except Exception as e:
            print(e)
            flag = 1
            time.sleep(1)

def sinle_test():
    '''一次测试'''
    #  redis 初始化库存量
    rcon.set('seckill', left)
    #  多线程模拟并发
    threads = []
    for i in range(tn):
        threads.append(threading.Thread(target=update_views))

    print('start')
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    #  redis查询剩余库存量
    res = rcon.get('seckill')
    res = int(res.decode())
    print(res)
    if res < 0:
        print(f'超卖 {res}')
        with open('log.txt', 'a', encoding='utf8') as f:
            f.write(f'{time.strftime("%H:%M:%S")}超卖 {res}\n')

if __name__ == '__main__':
    while True:
        sinle_test()
        time.sleep(200)
