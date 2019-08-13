from tornado.web import RequestHandler
class IndexHandler(RequestHandler):
    def get(self, *args, **kwargs):
        print('http方法')
        self.send_error(500)
        self.write('good man')

    def prepare(self, *args, **kwargs):
        print('prepare')
        self.write('very very man')

    def initialize(self, *args, **kwargs):
        print('initialize')

    def set_default_headers(self, *args, **kwargs):
        print('set_defualt_headers')

    def on_finish(self, *args, **kwargs) -> None:
        print('on_finish')

    def write_error(self, status_code, *args, **kwargs):
        print('write error')
        self.write('服务器内部错误')
#cookie
class PCookieHandler(RequestHandler):
    def get(self,*args,**kwargs):
        #设置
        self.set_cookie('sunck','good')
        # self.set_header('Set-Cookie','sunck=good1; Path=/')
        self.write('ok')

class GetPCookieHandler(RequestHandler):
    def get(self,*args,**kwargs):
        #获取一个cookie
        cookie=self.get_cookie('sunck','未登录')
        print('cookie',cookie)
        self.write('ok')

class ClearPCookieHandler(RequestHandler):
    def get(self,*args,**kwargs):
        #清除cookie
        self.clear_cookie('sunck')
        self.clear_all_cookies(path='/',domain=None)
        self.write('ok')

#安全cookie
class SCookieHandler(RequestHandler):
    def get(self,*args,**kwargs):
        self.set_secure_cookie('zhangmanyu','nice')
        self.write('ok')

class GetSCookieHandler(RequestHandler):
    def get(self,*args,**kwargs):
        scookie=self.get_secure_cookie('zhangmanyu')
        print(scookie)
        self.write('ok')

#cookie计数
class CookieNumHandler(RequestHandler):
    def get(self,*args,**kwargs):
        count=self.get_cookie('count',None)
        print(type(count),count)
        if not count:
            count=1
        else:
            count=int(count)
            count+=1
        print(count)
        self.set_cookie('count',str(count))
        self.render('cookienum.html',count=count)