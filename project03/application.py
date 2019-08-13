import tornado.web
from views import index
import config
import os
from ORM.sunckMysql import SunckMySQL

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            # (r'/',index.IndexHandler),
            # 渲染
            (r'/home', index.HomeHandler),
            # 函数
            (r'/function', index.FunctionHandler),
            # 转义
            (r'/trans', index.TransHandler),
            # 继承
            (r'/cart', index.CartHandler),
            # 数据库
            (r'/students', index.StudentHandler),

            # StaticFielHandler要放在所有路由的最下面
            (r'/(.*)$', tornado.web.StaticFileHandler,
             {"path": os.path.join(config.BASE_DIRS, 'static/html'), 'default_filename': 'index.html'})
        ]
        super(Application, self).__init__(handlers, **config.settings)
        self.db = SunckMySQL(**config.mysql)
