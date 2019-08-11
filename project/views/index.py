from tornado.web import RequestHandler

class IndexHandler(RequestHandler):
    def get(self,*args,**kwargs):
        url=self.reverse_url('kaige')
        self.write('<a href="%s">去另一个界面</a>'%url)
#
# class HomeHandler(RequestHandler):
#     def get(self,*args,**kwargs):
#         self.write('this is home ')

#重定向
class RedirectHandler(RequestHandler):
    def get(self,*args,**kwargs):
        self.redirect('/')


class SunckHandler(RequestHandler):
    #该方法会在HTTP方法(get,post)之前调用
    def initialize(self,word1,word2):
        self.word1=word1
        self.word2=word2
    def get(self,*args,**kwargs):
        # print(self.word1,self.word2)
        self.write('sunck is a nice man')
#get传参
class KaigeHandler(RequestHandler):
    def initialize(self,word3,word4):
        self.word3=word3
        self.word4=word4
    def get(self, *args, **kwargs):
        # print(self.word3, self.word4)
        self.write('sunck is a nice man')
class LiuyifeiHandler(RequestHandler):
    def get(self,p1,p2,*args,**kwargs):
        print(p1,p2,sep='-')
        self.write('liuyifei is a nice women')
class ZhangmanyuHandler(RequestHandler):
    def get(self,*args,**kwargs):
        a=self.get_query_argument('a')
        b = self.get_query_argument('b')
        c = self.get_query_argument('c')
        print(a,b,'*'+c+'*')
        self.write('zhangmanyu is good women')
#post请求，拿数据
class PostFileHandler(RequestHandler):
    def get(self,*args,**kwargs):
        self.render('postfile.html')
    def post(self,*args,**kwargs):
        name=self.get_body_argument('username')
        passwd=self.get_body_argument('passwd')
        hobbyList=self.get_body_arguments('hobby')
        print(name,passwd,hobbyList)
        self.write('sunck is a handsome man')
#request对象属性
class ZhuyingHandler(RequestHandler):
    def get(self,*args,**kwargs):
        print('method',self.request.method)
        print('host',self.request.host)
        print('url',self.request.uri)
        print('path',self.request.path)
        print('query',self.request.query)
        print('version',self.request.version)
        print('headers',self.request.headers)
        print('body',self.request.body)
        print('remote_ip',self.request.remote_ip)
        print('files',self.request.files)
        self.write('zhuyin is a good women')
#UpFile,文件上传
class UpFileHandler(RequestHandler):
    def get(self,*args,**kwargs):
        self.render('upfile.html')
    def post(self,*args,**kwargs):
        filesDict=self.request.files
        for inputname in filesDict:
            fileArr=filesDict[inputname]
            for fileObject in fileArr:
                import os
                import config
                #存储路径
                filePath=os.path.join(config.BASE_DIRS,'upfile/'+fileObject.filename)
                with open(filePath,'wb') as f:
                    f.write(fileObject.body)
        print(filesDict)
        self.write('ok')
#write
class WriteHandler(RequestHandler):
    def get(self,*args,**kwargs):
        self.write('good')
        self.write('nice')
        self.write('handsome')
        self.write('man')
        #刷新缓冲区,关闭当次请求通道
        #在finish()下面不要再写write，报错：RuntimeError: Cannot write() after finish()
        self.finish()
        self.write('right')
#json
class Json1Handler(RequestHandler):
    def get(self,*args,**kwargs):
        per={
            'name':'sunck',
            'age':18,
            'height':175,
            'weight':70
        }
        import json
        jsonStr=json.dumps(per)
        self.set_header('Content-Type','application/json;charset=utf-8')
        #自定义响应头属性
        self.set_header('sunck','hhgood')
        self.write(jsonStr)
class Json2Handler(RequestHandler):
    def get(self,*args,**kwargs):
        per={
            'name':'sunck',
            'age':18,
            'height':175,
            'weight':70
        }
        self.write(per)
class HeaderHandler(RequestHandler):
    #重写
    def set_default_headers(self):
        self.set_header('Content-Type','text/html;charset=utf-8')
        self.set_header('kaige','nice')
    def get(self,*args,**kwargs):
        self.set_header('kaige','handsome')
        self.write('good nice')
    def post(self,*args,**kwargs):
        pass
#状态码
class StatusCodeHandler(RequestHandler):
    def get(self,*args,**kwargs):
        self.set_status(200,'我是谁，我在哪里')
        self.write('88888888888888888888888888')



#错误处理
class ErrorHandler(RequestHandler):
    def write_error(self, status_code: int, **kwargs):
        if status_code==500:
            code=500
            #返回500界面（自定义）
            self.write('服务器内部错误')
        elif status_code==404:
            code=404
            #返回404界面(自定义)
            self.write('资料不存在')
        self.set_header(code)
    def get(self,*args,**kwargs):
        flag=self.get_query_argument('flag')
        if flag== '0':
            self.send_error(500) #执行这步之后就跳到self.write_error方法
        self.write('you are right')