#tornado 的基础web模块,
import tornado.web
#tornado的核心io循环模块,封装了linux的epoll，是tornado高效的基础
import tornado.ioloop
'''
tornado 的基础web模块,
'''
#引入
import tornado.httpserver
#类比Django中的视图
#一个业务处理类
class IndexHandler(tornado.web.RequestHandler):

    def get(self,*args,**kwargs):

        self.write('sunck is a good man ')
if __name__=='__main__':
    app=tornado.web.Application([
            (r'/',IndexHandler)
    ])
 #   app.listen(8000)
    #实例化一个http对象
    httpServer=tornado.httpserver.HTTPServer(app)
    #绑定端口
    httpServer.listen(8000)
    tornado.ioloop.IOLoop.current().start()