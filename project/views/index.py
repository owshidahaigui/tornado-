from tornado.web import RequestHandler

class IndexHandler(RequestHandler):
    def get(self,*args,**kwargs):
        url=self.reverse_url('kaige')
        self.write('<a href="%s">去另一个界面</a>'%url)
#
# class HomeHandler(RequestHandler):
#     def get(self,*args,**kwargs):
#         self.write('this is home ')

class SunckHandler(RequestHandler):
    #该方法会在HTTP方法(get,post)之前调用
    def initialize(self,word1,word2):
        self.word1=word1
        self.word2=word2
    def get(self,*args,**kwargs):
        # print(self.word1,self.word2)
        self.write('sunck is a nice man')

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