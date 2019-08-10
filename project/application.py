import tornado.web
from  views import index
import config
class Application(tornado.web.Application):
    def __init__(self):
        handlers=[
            (r'/',index.IndexHandler),
            (r'/sunck',index.SunckHandler,{'word1':"good",'word2':'nice'}),
            tornado.web.url(r'/kaige',index.KaigeHandler,{'word3':"handsome",'word4':'cool'},name='kaige'),
            (r'/liuyifei/(?P<p1>\w+)/(?P<p2>\w+)/(?P<p3>\w+)',index.LiuyifeiHandler),
            (r'/zhangmanyu',index.ZhangmanyuHandler)
        ]
        super(Application,self).__init__(handlers,**config.settings)