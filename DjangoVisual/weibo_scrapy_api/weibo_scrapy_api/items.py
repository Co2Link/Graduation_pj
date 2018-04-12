# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboScrapyApiItem(scrapy.Item):
    user=scrapy.Field()
    master_id=scrapy.Field()

class UserItem(scrapy.Item):
    id=scrapy.Field()

    description=scrapy.Field()
    follow_count=scrapy.Field()
    followers_count=scrapy.Field()
    gender=scrapy.Field()
    statuses_count=scrapy.Field()
    verified_type=scrapy.Field()
    screen_name=scrapy.Field()

    location=scrapy.Field()

    avatar_hd=scrapy.Field()

class fans_1_Item(scrapy.Item):
    master_id=scrapy.Field()

    sid=scrapy.Field()
    follow_count=scrapy.Field()
    followers_count=scrapy.Field()
    gender=scrapy.Field()
    statuses_count=scrapy.Field()
    verified_type=scrapy.Field()
    screen_name=scrapy.Field()

    location=scrapy.Field()

    description=scrapy.Field()
    #new
    mbrank=scrapy.Field()
    mbtype=scrapy.Field()
class fans_2_Item(scrapy.Item):
    page=scrapy.Field()
    master_id=scrapy.Field()

class post_Item(scrapy.Item):
    page=scrapy.Field()

class comment_Item(scrapy.Item):
    page=scrapy.Field()
    post_id=scrapy.Field()



