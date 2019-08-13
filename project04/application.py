import tornado.web
from views import index
import config
import os
from ORM.sunckMysql import SunckMySQL

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/',index.IndexHandler),
            #普通cookie
            (r'/pcookie',index.PCookieHandler),
            (r'/getpcookie',index.GetPCookieHandler),
            (r'/clearpcookie',index.ClearPCookieHandler),
            #安全cookie
            (r'/scookie',index.SCookieHandler),
            (r'/getscookie',index.GetSCookieHandler),
            #cookie计数,记录浏览器访问次数
            (r'/cookienum',index.CookieNumHandler),
        ]
        super(Application, self).__init__(handlers, **config.settings)
