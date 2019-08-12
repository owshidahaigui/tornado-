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


class HomeHandler(RequestHandler):
    def get(self, *args, **kwargs):
        temp = 100
        dict = {'name': 'tom', 'age': 18}
        self.render('home.html', num=temp, per=dict)


# 自定义函数
class FunctionHandler(RequestHandler):
    def get(self, *args, **kwargs):
        def mySum(n1, n2):
            return n1 + n2

        self.render('home.html', mySum=mySum)


class TransHandler(RequestHandler):
    def get(self, *args, **kwargs):
        str = '<h1>sunck is a good man </h1>'
        self.render('trans.html', str=str)


class CartHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render('cart.html', title='cart')


# 数据库
class StudentHandler(RequestHandler):
    def get(self, *args, **kwargs):
        # 去数据库提取数据
        stus = self.application.db.get_all_obj('select * from students','students')
        print(stus)
        self.write('ok')
        # self.render('students.html', stus=stus)
