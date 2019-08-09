# tornado

第一个实例

```Python
#server01.py
#tornado 的基础web模块,
import tornado.web
#tornado的核心io循环模块,封装了linux的epoll，是tornado高效的基础
import tornado.ioloop
#类比Django中的视图
#一个业务处理类
class IndexHandler(tornado.web.RequestHandler):
    #处理get请求，不能处理POST请求
    def get(self,*args,**kwargs):
        #对应http1请求的方法
        #给浏览器响应信息
        self.write('sunck is a good man ')
if __name__=='__main__':
    #实例化一个app对象
    #application ：是tornado web框架的核心应用类,s是与服务器对应的接口
    #里面保存了路由映射表，有一个linsten方法，用了创建一个http服务器的实例并绑定了端口
    app=tornado.web.Application([
            (r'/',IndexHandler)
    ])
    #绑定监听端口
    #注意：此时服务器并没有开启监听
    app.listen(8000)
    '''
    IOLoop.current():返回当前线程的IOLoop实例
    IOLoop.start():启动IOlOOP实例的I/O循环，同时开启监听
    '''
    tornado.ioloop.IOLoop.current().start()
```

## 单进程与多进程

tornado默认启动单进程

- httpServer=tornado.httpserver.HTTPServer(app)
- httpServer.bind(port) 绑定端口
- httpServer.start(num) 启动num个进程，缺省默认为1，值为None,或者小于0，开启对应硬件机器的cpu核心数的进程
- app.listen() 只能在单进程模式中使用
- 多进程 虽然tornado 给我们提供了一次性启动多进程的方式，但是由于一些问题，不建议使用多进程实例的方式启动多进程，而是==手动启动多进程==，还能绑定多个端口
- 为什么不那样启动多进程：
  	1. 每个子进程都会从父进程中辅助一份IOloop的实例，如果在创建子进程前修改了IOloop，会影响所有的子进程
   	2. 所有的进程都是由一个命令，无法做到在不停止服务的情况下修改代码
   	3. 所有进程共享一个端口，想要分别监控很困难

### 多进程实例

```python
#server03.py
import tornado.web
import tornado.ioloop
import tornado.httpserver
class IndexHandler(tornado.web.RequestHandler):
    def get(self,*args,**kwargs):
        self.write('sunck is a good man ')
if __name__=='__main__':
    app=tornado.web.Application([
            (r'/',IndexHandler)
    ])
    #app.listen(8000) #这个就是默认监听8000借口并且开启服务器1个进程
    httpServer=tornado.httpserver.HTTPServer(app)
    #将服务器绑定到8000端口
    #httpServer.listen(8000)
    httpServer.bind(8000)
    #启动5个进程，缺省默认为1，值为None,或者小于0，开启对应硬件机器的cpu核心数的进程
    httpServer.start(5)
    tornado.ioloop.IOLoop.current().start()
```

