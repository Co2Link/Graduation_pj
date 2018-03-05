from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class my_model(models.Model):
    id=models.IntegerField(primary_key=True)
    body=models.TextField()
    num=models.IntegerField(null=True)


class Post(models.Model):
    title = models.CharField(max_length=70)
    body = models.TextField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    excerpt = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    def get_absolute_url(self): # reverse: 解析该视图函数对应的url，并且传入url所需的值
        return reverse('blog:detail', kwargs={'pk': self.pk}) #视图函数命名空间+视图函数别名=blog:detail
