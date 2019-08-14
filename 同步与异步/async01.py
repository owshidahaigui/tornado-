import time
import threading

# handler,耗时操作数据库查询等操作
def longIo(callback):
    def run(cb):
        print('开始耗时操作')
        time.sleep(5)
        print('结束耗时操作')
        cb('sunck is good man')
    #创建一个线程进行异步操作
    threading.Thread(target=run,args=(callback,)).start()

#回调函数，异步操作，类似ajax的success：函数
def finish(data):
    print('开始处理回调函数')
    print('接收到longio的响应数据：',data)
    print('结束处理回调函数')

# 一个客户端的请求
def reaA():
    print('开始处理reqA')
    longIo(finish)
    print('结束处理reqA')

# 另一个客户端的请求
def reaB():
    print('开始处理reqB')
    time.sleep(2)
    print('结束处理reqB')

# tornado服务
def main():
    reaA()
    reaB()
    while 1:
        time.sleep(0.1)
        pass

if __name__ == '__main__':
    main()