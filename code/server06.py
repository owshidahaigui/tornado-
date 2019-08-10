import tornado.web
import tornado.ioloop
import tornado.httpserver
import config
class IndexHandler(tornado.web.RequestHandler):
    def get(self,*args,**kwargs):
        self.write('sunck is a good man ')
if __name__=='__main__':
    print('list',config.options['list'])
    app=tornado.web.Application([
            (r'/',IndexHandler)
    ])
    httpServer=tornado.httpserver.HTTPServer(app)
    httpServer.bind(config.options['port'])
    httpServer.start(1)
    tornado.ioloop.IOLoop.current().start()