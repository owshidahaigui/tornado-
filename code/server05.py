import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import options
#函数的原型
#定义2个参数
tornado.options.define('port',default=8000,type=int,help="this is a port",metavar=None,multiple=False,group=None,callback=None)
#常用参数,设置变量为list ，传入列表，列表元素为字符串类型
tornado.options.define('list',default=[],type=str,multiple=True)
class IndexHandler(tornado.web.RequestHandler):
    def get(self,*args,**kwargs):
        self.write('sunck is a good man ')
if __name__=='__main__':
    #转换命令行参数，并保存到tornado.options.options
    tornado.options.parse_config_file('config')
    #关闭日志
    tornado.options.options.logging=None
    print('list',tornado.options.options.list)
    app=tornado.web.Application([
            (r'/',IndexHandler)
    ])
    httpServer=tornado.httpserver.HTTPServer(app)
    #使用变量的值
    httpServer.bind(tornado.options.options.port)
    httpServer.start(1)
    tornado.ioloop.IOLoop.current().start()