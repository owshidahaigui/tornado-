import time
import threading

gen=None
# handler,耗时操作数据库查询等操作
def longIo():
    def run():
        print('开始耗时操作')
        time.sleep(5)
        try:
            global gen
            gen.send('sunck is a good man')
        except:
            pass
    #创建一个线程进行异步操作
    threading.Thread(target=run).start()

# 一个客户端的请求
def reaA():
    print('开始处理reqA')
    res= yield longIo()
    print('接收到longio的响应数据：',res)
    print('结束处理reqA')

# 另一个客户端的请求
def reaB():
    print('开始处理reqB')
    time.sleep(2)
    print('结束处理reqB')

# tornado服务
def main():
    global gen
    gen=reaA()#生成一个生成器
    next(gen)#执行reqA
    reaB()
if __name__ == '__main__':
    main()