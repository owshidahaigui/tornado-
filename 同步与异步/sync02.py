import time
import threading
#handler
def longIo():
    print('开始耗时操作')
    time.sleep(5)
    print('结束耗时操作')



#一个客户端的请求
def reaA():
    print('开始处理reqA')
    print('结束处理reqA')

#另一个客户端的请求
def reaB():
    print('开始处理reqB')
    print('结束处理reqB')

#tornado服务
def main():
    reaA()
    reaB()
    while 1:
        time.sleep(0.1)
        pass

if  __name__=='__main__':
    main()