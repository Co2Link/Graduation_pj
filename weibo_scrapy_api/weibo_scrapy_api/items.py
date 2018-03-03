# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboScrapyApiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
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
    # reg_time=scrapy.Field()

class fans_1_Item(scrapy.Item):
    master_id=scrapy.Field()

    id=scrapy.Field()
    follow_count=scrapy.Field()
    followers_count=scrapy.Field()
    gender=scrapy.Field()
    statuses_count=scrapy.Field()
    verified_type=scrapy.Field()
    screen_name=scrapy.Field()

    location=scrapy.Field()
    # reg_time=scrapy.Field()
class fans_2_Item(scrapy.Item):
    master_id=scrapy.Field()
    id=scrapy.Field()
    follow_count=scrapy.Field()
    followers_count=scrapy.Field()
    statuses_count=scrapy.Field()
    verified_type=scrapy.Field()

class post_Item(scrapy.Item):
    # id=scrapy.Field()
    # author_id=scrapy.Field()
    # attitudes_count=scrapy.Field()
    # comments_count=scrapy.Field()
    # created_at=scrapy.Field()
    # pics=scrapy.Field()
    # reposts_count=scrapy.Field()
    # source=scrapy.Field()
    # text=scrapy.Field()
    page=scrapy.Field()



