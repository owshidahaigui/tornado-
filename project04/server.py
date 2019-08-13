import tornado.ioloop
import tornado.httpserver
import config
from application import Application

if __name__=='__main__':
    app=Application()
    httpServer=tornado.httpserver.HTTPServer(app)
    httpServer.bind(config.options['port'])
    httpServer.start(1)
    tornado.ioloop.IOLoop.current().start()