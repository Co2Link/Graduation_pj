from django.db import models

# Create your models here.

class ScrapyItem(models.Model):
    id=models.IntegerField(primary_key=True)
    task_id=models.CharField(max_length=50)

class UserItem_dj(models.Model):
    id=models.CharField(max_length=100,primary_key=True)

    description=models.CharField(max_length=150)
    follow_count=models.IntegerField()
    followers_count=models.IntegerField()
    gender=models.CharField(max_length=1)
    statuses_count=models.IntegerField()
    verified_type=models.IntegerField()
    screen_name=models.CharField(max_length=30)

    location=models.CharField(max_length=50)
    def __str__(self):
        return str(self.id)

class fans_1_Item_dj(models.Model):
    master_id=models.CharField(max_length=100)

    id=models.CharField(max_length=100,primary_key=True)
    follow_count = models.IntegerField()
    followers_count = models.IntegerField()
    gender = models.CharField(max_length=1)
    statuses_count = models.IntegerField()
    verified_type=models.IntegerField()
    screen_name = models.CharField(max_length=30)

    location=models.CharField(max_length=50)
    def __str__(self):
        return str(self.id)

class fans_2_Item_dj(models.Model):
    master_id = models.CharField(max_length=100)
    id = models.CharField(max_length=100,primary_key=True)
    follow_count = models.IntegerField()
    followers_count = models.IntegerField()
    statuses_count = models.IntegerField()
    verified_type=models.IntegerField()
    def __str__(self):
        return str(self.id)

class post_Item_dj(models.Model):
    author_id=models.IntegerField()
    attitudes_count=models.IntegerField()
    comments_count=models.IntegerField()
    created_at=models.CharField(max_length=20)
    created_at_org=models.CharField(max_length=20)
    id=models.IntegerField(primary_key=True)
    pics=models.BooleanField()
    reposts_count=models.IntegerField()
    source=models.CharField(max_length=50)
    text=models.TextField()
    retweeted_status=models.BooleanField()
    retweeted_text=models.TextField(null=True)
    def __str__(self):
        return str(self.id)