import tornado.web
from views import index
import config
import os
from ORM.sunckMysql import SunckMySQL

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [

            #普通cookie
            (r'/pcookie',index.PCookieHandler),
            (r'/getpcookie',index.GetPCookieHandler),
            (r'/clearpcookie',index.ClearPCookieHandler),
            #安全cookie
            (r'/scookie',index.SCookieHandler),
            (r'/getscookie',index.GetSCookieHandler),
            #cookie计数,记录浏览器访问次数
            (r'/cookienum',index.CookieNumHandler),
            (r'/postfile',index.PostFileHandler),

            #设置_xsrf的cookie
            (r'/setxsrfcookie',index.SetXSRFCookieHandler),
            #用户验证
            (r'/login',index.LoginHandler),
            (r'/home',index.HomeHandler),
            (r'/cart',index.CartHandler),
            (r'/(.*)',index.StaticFileHandler,{'path':os.path.join(config.BASE_DIRS,'static/html'),'default_filename':'index.html'})
        ]
        super(Application, self).__init__(handlers, **config.settings)
