from tornado.web import RequestHandler
import tornado.web
import tornado.gen
import time

class StaticFileHandler(tornado.web.StaticFileHandler):
    def __init__(self,*args,**kwargs):
        super(StaticFileHandler,self).__init__(*args,**kwargs)
        self.xsrf_token
#cookie
from tornado.httpclient import AsyncHTTPClient
class StudentsHandler(RequestHandler):

    def on_response(self,response):
        if response.error:
            self.send_error(500)
        else:
            import json
            data=json.loads(response.body)
            self.write(data)
        self.finish()
    def get(self,*args,**kwargs):
        #获取学生信息
        # time.sleep(10)
        #创建异步客户端
        client=AsyncHTTPClient()
        client.fetch('http://fanyi.youdao.com/',self.on_response)
        # self.write('ok')

class HomeHandler(RequestHandler):
    def get(self,*args,**kwargs):
        self.write('home')

class Student02Hanler(RequestHandler):
    @tornado.gen.coroutine
    def get(self,*args,**kwargs):
        client = AsyncHTTPClient()
        res= yield client.fetch('http://fanyi.youdao.com/')
        if res.error:
            self.send_error(500)
        else:
            import json
            data=res.body
      #      data=json.loads(res.body)
            self.write(data)

class Student03Handler(RequestHandler):
    @tornado.gen.coroutine
    def get(self,*args,**kwargs):
        res =yield self.getData()
        self.write(res)

    @tornado.gen.coroutine
    def getData(self):
        client = AsyncHTTPClient()
        res = yield client.fetch('http://fanyi.youdao.com/')
        if res.error:
            ret={'ret':0}
        else:
            ret=res.body
        raise tornado.gen.Return(ret)