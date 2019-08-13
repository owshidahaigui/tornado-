
from ORM.orm import ORM
class Students(ORM):
    def __init__(self,name,age):
        self.name=name
        self.age=age