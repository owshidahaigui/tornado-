#tornado 的基础web模块,
import tornado.web
#tornado的核心io循环模块,封装了linux的epoll，是tornado高效的基础
import tornado.ioloop
'''
tornado 的基础web模块,
'''
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