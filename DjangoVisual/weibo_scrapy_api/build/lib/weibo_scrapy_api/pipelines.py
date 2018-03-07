# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo as pymongo
import logging
import datetime
import re
from .items import UserItem,fans_2_Item,fans_1_Item,post_Item
from scrapy.exceptions import DropItem
from my_main.models import UserItem_dj,fans_1_Item_dj,fans_2_Item_dj,post_Item_dj
def clean_time(time):
    today = datetime.datetime.now().date()
    if '小时' in time:  # x分钟前；x小时前
        hours=int(re.search('(\d+)',time).group(1))
        if hours>datetime.datetime.now().hour:  #昨天
            time = str(today-datetime.timedelta(days=1))
        else:
            time=str(today)
    elif '分钟' in time:
        minutes=int(re.search('(\d+)',time).group(1))
        if datetime.datetime.now().hour==0 and minutes>datetime.datetime.now().minute:   #昨天
            time=str(today-datetime.timedelta(days=1))
        else:
            time=str(today)
    elif '昨' in time:  # 昨天 xx
        yesterday = today - datetime.timedelta(days=1)
        time = str(yesterday)
    elif len(time) == 5:  # xx-xx  (02-01) 2月1号
        this_year = str(today)[:5] + time
        time = this_year
    elif len(time)!=10:
        time=None
    return time

def clean_dict(my_dict, attr_list):  #数据整理，清洗
    my_dict_clean={}
    for attr in attr_list:
        if attr=='created_at':                 #统一化时间显示
            my_dict_clean[attr]=clean_time(my_dict[attr])
            my_dict_clean['created_at_org']=my_dict[attr]
        elif attr=='pics':
            my_dict_clean['pics']=('pics' in my_dict)
        elif attr=='author_id':
            my_dict_clean['author_id']=my_dict['user']['id']
        elif attr=='retweeted_status':          #转发微博的信息
            if 'retweeted_status'in my_dict:
                my_dict_clean['retweeted_status']=True
            else:
                my_dict_clean['retweeted_status'] = False
        else:
            my_dict_clean[attr] = my_dict[attr]

    return my_dict_clean

def fans_2_to_dict(my_dict,attr_list,master_id):
    my_dict_clean={}
    my_dict_clean['master_id']=master_id
    for attr in attr_list:
        my_dict_clean[attr]=my_dict[attr]
    return my_dict_clean



class WeiboScrapyApiPipeline(object):
    def __init__(self):
        #数据库操作
        self.CONN=pymongo.MongoClient('localhost',27017)
        self.DBNAME='syn_7'
        self.user_col=self.CONN[self.DBNAME]['user']
        self.fans_1_col=self.CONN[self.DBNAME]['fans_1']
        self.fans_2_col=self.CONN[self.DBNAME]['fans_2']
        self.post_col=self.CONN[self.DBNAME]['post']
        self.user_col.create_index([('id', pymongo.ASCENDING)], unique=True)
        self.fans_1_col.create_index([('id', pymongo.ASCENDING)], unique=True)
        self.fans_2_col.create_index([('id', pymongo.ASCENDING)], unique=True)
        self.post_col.create_index([('id', pymongo.ASCENDING)], unique=True)
        #debug变量
        self.count_user=0
        self.count_fans_1=0
        self.count_fans_2=0
    def process_item(self, item, spider):
        if isinstance(item,UserItem):               # User
            self.count_user+=1
            try:
                item_dj=UserItem_dj(**item)
                item_dj.save()
            except Exception as e:
                logging.warning(('dj_1',str(e)))

            try:
                self.user_col.insert_one(dict(item))
            except Exception as e:
                logging.debug(('Exception_1',str(e)))
        elif isinstance(item,fans_1_Item):              #fans_1
            self.count_fans_1+=1
            try:
                item_dj=fans_1_Item_dj(**item)
                item_dj.save()
            except Exception as e:
                logging.warning(('dj_2',str(e)))
            try:
                self.fans_1_col.insert_one(dict(item))
            except Exception as e:
                logging.debug(('Exception_2',str(e)))
        elif isinstance(item,fans_2_Item):              #fans_2
            # try:
            #     item_dj=fans_2_Item_dj(**item)
            #     item_dj.save()
            # except Exception as e:
            #     logging.warning(('dj_3',str(e)))
            # self.count_fans_2+=1
            # try:
            #     self.fans_2_col.insert_one(dict(item))
            # except Exception as e:
            #     logging.debug(('Exception_3',str(e)))
            page=item['page']
            master_id=item['master_id']
            item_list=[]
            card_list = []
            attr_list=['id','follow_count','followers_count','statuses_count','verified_type']
            for card in page:
                if card['card_type']==10:
                    user=card['user']
                    card_list.append(fans_2_to_dict(user,attr_list,master_id))
                    item_list.append(fans_2_Item_dj(**fans_2_to_dict(user,attr_list,master_id)))
            try:
                fans_2_Item_dj.objects.bulk_create(item_list)
            except Exception as e:
                logging.warning(('fans_2_error',str(e)))
            try:
                result = self.fans_2_col.insert_many(card_list, ordered=False)
            except pymongo.errors.BulkWriteError as e:
                logging.debug(('BulkWriteError: ', str(e)))


        elif isinstance(item,post_Item):                   #post
            attr_list = ['author_id', 'attitudes_count', 'comments_count', 'created_at', 'id', 'pics', 'reposts_count',
                         'source', 'text', 'retweeted_status']
            page = item['page']
            card_list = []
            item_list=[]
            for card in page:
                if card['card_type'] == 9:
                    my_dict=clean_dict(card['mblog'], attr_list)
                    card_list.append(my_dict)
                                                            # dj
                    item_list.append(post_Item_dj(**my_dict))
                    # try:
                    #     item_dj=post_Item_dj(**my_dict)
                    #     item_dj.save()
                    # except Exception as e:
                    #     logging.warning(('dj_4', str(e)))
            try:
                post_Item_dj.objects.bulk_create(item_list)
            except Exception as e:
                logging.warning(('post_error',str(e)))
            try:
                result = self.post_col.insert_many(card_list, ordered=False)
            except pymongo.errors.BulkWriteError as e:
                logging.debug(('BulkWriteError: ', str(e)))
        return DropItem()

    def close_spider(self,spider):
        logging.debug(('count_user',self.count_user))
        logging.debug(('count_fans_1',self.count_fans_1))
        logging.debug(('count_fans_2',self.count_fans_2))
