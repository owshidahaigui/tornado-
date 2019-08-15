import time
import threading


# handler,耗时操作数据库查询等操作
def longIo():
    print('开始耗时操作')
    time.sleep(5)
    print('结束限时操作')
   #返回数据
    yield 'sunck is a good man'


#定义运行生成器的装饰器
def genCoroutine(func):
    def wrapper(*args,**kwargs):
        gen1 = func()  # 生成reqA的生成器
        gen2=next(gen1)  # longIo的生成器
        def run(g):
            res=next(g)
            try:
                gen1.send(res)#返回给regA数据
            except StopIteration as e:
                pass
        threading.Thread(target=run,args=(gen2,)).start()
    return  wrapper

# 一个客户端的请求
@genCoroutine
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
    reaA()
    reaB()
if __name__ == '__main__':
    main()