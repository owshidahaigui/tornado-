import tornado.web
from views import index
import config
import os
from ORM.sunckMysql import SunckMySQL

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [

            (r'/students',index.StudentsHandler),
            (r'/students02',index.Student02Hanler),
            (r'/students03',index.Student03Handler),
            (r'/home',index.HomeHandler),
            (r'/(.*)',index.StaticFileHandler,{'path':os.path.join(config.BASE_DIRS,'static/html'),'default_filename':'index.html'})
        ]
        super(Application, self).__init__(handlers, **config.settings)
