from django.db import models

# Create your models here.

class ScrapyItem(models.Model):
    id=models.CharField(max_length=100,primary_key=True)
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

    avatar_hd=models.TextField(null=True)
    def __str__(self):
        return str(self.id)
class fans_1_Item_dj(models.Model):
    master_id=models.CharField(max_length=100)

    sid=models.CharField(max_length=100)
    follow_count = models.IntegerField()
    followers_count = models.IntegerField()
    gender = models.CharField(max_length=1)
    statuses_count = models.IntegerField()
    verified_type=models.IntegerField()
    screen_name = models.CharField(max_length=30)

    location=models.CharField(max_length=50)

    description = models.CharField(max_length=150,null=True)

    #new
    mbrank=models.IntegerField()
    mbtype=models.IntegerField()
    def __str__(self):
        return str(self.sid)
    class Meta:
        unique_together = ("sid", "master_id")

class fans_2_Item_dj(models.Model):
    master_id = models.CharField(max_length=100)
    sid = models.CharField(max_length=100)
    follow_count = models.IntegerField()
    followers_count = models.IntegerField()
    statuses_count = models.IntegerField()
    verified_type=models.IntegerField()

    #new
    mbrank=models.IntegerField()
    mbtype=models.IntegerField()
    screen_name=models.CharField(max_length=100)

    description = models.CharField(max_length=150, null=True)
    def __str__(self):
        return str(self.sid)
    class Meta:
        unique_together = ("sid", "master_id")

class post_Item_dj(models.Model):
    author_id=models.CharField(max_length=100,null=True)
    attitudes_count=models.IntegerField()
    comments_count=models.IntegerField()
    created_at=models.CharField(max_length=20)
    created_at_org=models.CharField(max_length=20,null=True)
    id=models.CharField(max_length=100,primary_key=True)
    pics=models.BooleanField(default=False)
    reposts_count=models.IntegerField()
    source=models.CharField(max_length=50,null=True)
    text=models.TextField()
    retweeted_status=models.BooleanField()
    retweeted_text=models.TextField(null=True)

    def __str__(self):
        return str(self.id)

class new_post_Item_dj(models.Model):
    attitudes_count=models.IntegerField()
    comments_count=models.IntegerField()
    created_at=models.CharField(max_length=20)
    id=models.CharField(max_length=100,primary_key=True)
    reposts_count=models.IntegerField()
    text=models.TextField()
    retweeted_status=models.BooleanField()
    retweeted_text=models.TextField(null=True)

    def __str__(self):
        return str(self.id)

class comments_Item_dj(models.Model):
    created_at=models.CharField(max_length=20)
    id=models.CharField(max_length=100,primary_key=True)
    like_counts=models.IntegerField()
    source=models.CharField(max_length=50,null=True)
    text=models.TextField()
    user_id=models.CharField(max_length=100)
    screen_name=models.CharField(max_length=30)
    post_id=models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)