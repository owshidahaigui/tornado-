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