import tornado.web
from views import index
import config
class Application(tornado.web.Application):
    def __init__(self):
        handlers=[
            (r'/',index.IndexHandler),
            (r'/sunck',index.SunckHandler,{'word1':"good",'word2':'nice'}),
            tornado.web.url(r'/kaige',index.KaigeHandler,{'word3':"handsome",'word4':'cool'},name='kaige'),
            (r'/liuyifei/(?P<p1>\w+)/(?P<p2>\w+)/(?P<p3>\w+)',index.LiuyifeiHandler),
            #get
            (r'/zhangmanyu',index.ZhangmanyuHandler),
            #post
            (r'/postfile',index.PostFileHandler),
            #request对象
            (r'/zhuyin',index.ZhuyingHandler),
            #上传文件
            (r'/upfile',index.UpFileHandler),
            #write
            (r'/write',index.WriteHandler),
            #json
            (r'/json1',index.Json1Handler),
            (r'/json2', index.Json2Handler),
            #header
            (r'/header',index.HeaderHandler),
            #状态码
            (r'/status',index.StatusCodeHandler),
            #重定向
            (r'/index',index.RedirectHandler),
            #错误处理
            #iserror?flag=2,tongg
            (r'/error',index.ErrorHandler),
        ]
        super(Application,self).__init__(handlers,**config.settings)