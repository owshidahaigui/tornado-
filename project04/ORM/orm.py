from tornado.web import RequestHandler
from .sunckMysql import SunckMySQL

class ORM(RequestHandler):
    def save(self):
        'insert into students(name, age)values("dahaigui", 30)'
        pass
        # self.application.db.insert(sql)

    def delete(self):
        pass

    def update(self):
        pass

    def all(self):
        pass

    def filter(self):
        pass