from mongoengine import *
from mytest.settings import DBNAME  #数据库名
connect(DBNAME) #链接数据库
class Post(Document):
    title = StringField(max_length=120, required=True)
    content = StringField(max_length=500, required=True)
    last_update = DateTimeField(required=True)

# Create your models here.
