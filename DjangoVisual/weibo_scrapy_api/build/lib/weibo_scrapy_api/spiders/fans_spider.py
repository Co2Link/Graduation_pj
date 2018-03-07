import scrapy
import json
import logging
from ..items import WeiboScrapyApiItem,UserItem,fans_1_Item,fans_2_Item,post_Item
class fans_spider(scrapy.Spider):
    name='fans'
    def __init__(self,*args,**kwargs):
        super(fans_spider,self).__init__(*args,**kwargs)
        self.fans_urls='https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{}&since_id={}'   #fans
        self.user_urls='https://m.weibo.cn/api/container/getIndex?containerid=100505{}'             #user基本信息_2
        self.info_urls='https://m.weibo.cn/api/container/getIndex?containerid=230283{}_-_INFO'      #user基本信息_1
        self.post_urls='https://m.weibo.cn/api/container/getIndex?value={}&containerid=107603{}&page={}'    #post
        self.id=kwargs.get('id')

    def start_requests(self):
        yield scrapy.Request(url=self.info_urls.format(self.id))
        for page in range(1,11):                                              #每个用户固定爬10页微博
            yield scrapy.Request(url=self.post_urls.format(self.id, self.id,page),callback=self.parse_post)
    def parse_post(self,response):
        result=json.loads(response.text)['data']['cards']
        if result!=[]:
            item = post_Item()
            item['page'] = result
            yield item
    def parse(self,response):   #info_urls   先获取user的所在地与注册时间
        cards=json.loads(response.text)['data']['cards']
        check=0     #检测用户是否存在
        for card in cards:
            if 'card_group' in card:
                for sub_card in card['card_group']:
                    if 'item_name' in sub_card and sub_card['item_name'] == '所在地':
                        location=sub_card['item_content']
                        check=1
                    # if sub_card['item_name']=='注册时间':
                    #     reg_time=sub_card['item_content']
                    #     check=2
        if check:
            yield scrapy.Request(url=self.user_urls.format(self.id), callback=self.parse_1,meta={'location': location})
        else:
            logging.warning('用户不存在')


    def parse_1(self, response): #user_urls    获取user其他的基本信息并且计算粉丝页数
        result=json.loads(response.text)
        try:
            user_info = result['data']['userInfo']
        except KeyError as e:
            logging(('KeyError',str(e)))
        item=UserItem()     #User
        item['location']=response.meta['location']
        # item['reg_time']=response.meta['reg_time']
        item['id']=self.id
        item['description']=user_info['description']
        item['follow_count']=user_info['follow_count']
        item['followers_count'] = user_info['followers_count']
        item['gender'] = user_info['gender']
        item['statuses_count'] = user_info['statuses_count']
        item['verified_type'] = user_info['verified_type']
        item['screen_name']=user_info['screen_name']
        yield item

        try:
            fans_num=user_info['followers_count']
        except KeyError as e:
            logging(('KeyError', str(e)))
        if int(fans_num/20)>250:
            pages=250
        else:
            pages=int(fans_num/20)+1
        logging.debug(('pages',pages))
        for i in range(1,pages+2):  #经实验，页数基本在（fans_num/20,(fans_num/20)+2)这个区间
            yield scrapy.Request(url=self.fans_urls.format(self.id,i),callback=self.parse_fans_1)

    def parse_fans_1(self,response): #fans_urls  获取粉丝基本信息,并且继续发出爬取下一层粉丝的请求
        result=json.loads(response.text)['data']['cards']
        if result!=[]:
            try:
                card_group=result[0]['card_group']
                for card in card_group:
                    if card['card_type'] == 10:
                        user = card['user']
                        master_id = self.id
                        id = user['id']
                        follow_count = user['follow_count']
                        followers_count = user['followers_count']
                        gender = user['gender']
                        statuses_count = user['statuses_count']
                        verified_type = user['verified_type']
                        screen_name = user['screen_name']
                        # 下面一句会报 ‘dictionary update sequence element #0 has length 9; 2 is required’的错误
                        # yield scrapy.Request(url=self.info_urls.format(id),callback=self.parse_fans_2,meta={'master_id':self.id,'id':user['id'],'follow_count':user['follow_count'],'followers_count':user['followers_count'],'gender':user['gender'],'statuses_count':user['statuses_count'],'verified_type':user['verified_type']})
                        yield scrapy.Request(url=self.info_urls.format(id), callback=self.parse_fans_2,
                                             meta={'master_id': master_id, 'id': id, 'follow_count': follow_count,
                                                   'followers_count': followers_count, 'gender': gender,
                                                   'statuses_count': statuses_count, 'verified_type': verified_type,
                                                   'screen_name': screen_name})
                        yield scrapy.Request(url=self.fans_urls.format(id, 1), callback=self.parse_fans_3,
                                             meta={'master_id': id})
            except KeyError as e:
                logging(str(e))

    def parse_fans_2(self,response):    #info_urls  获取第一层粉丝的所在地与注册时间
        cards = json.loads(response.text)['data']['cards']
        location='其他'
        for card in cards:
            if 'card_group'in card:
                for sub_card in card['card_group']:
                    if 'item_name'in sub_card and sub_card['item_name'] == '所在地':
                        location = sub_card['item_content']
                    # if sub_card['item_name'] == '注册时间':
                    #     reg_time = sub_card['item_content']
        item=fans_1_Item()      #第一层粉丝
        item['master_id']=response.meta['master_id']
        item['id']=response.meta['id']
        item['follow_count']=response.meta['follow_count']
        item['followers_count']=response.meta['followers_count']
        item['gender']=response.meta['gender']
        item['statuses_count']=response.meta['statuses_count']
        item['verified_type']=response.meta['verified_type']
        item['screen_name']=response.meta['screen_name']
        item['location']=location

        # item['reg_time']=reg_time
        yield item

    def parse_fans_3(self,response):       #fans_urls 获取粉丝的第一页粉丝
        result=json.loads(response.text)['data']['cards']
        if result!=[]:
            try:
                card_group=result[0]['card_group']
                item=fans_2_Item()
                item['page']=card_group
                item['master_id']=response.meta['master_id']
                yield item
                # for card in card_group:
                #     if card['card_type'] == 10:
                        # user = card['user']
                        # item = fans_2_Item()  # 第二层粉丝
                        # item['master_id'] = response.meta['master_id']
                        # item['id'] = user['id']
                        # item['followers_count'] = user['followers_count']
                        # item['follow_count'] = user['follow_count']
                        # item['statuses_count'] = user['statuses_count']
                        # item['verified_type'] = user['verified_type']
                        # yield item
            except KeyError as e:
                logging.warning(str(e))







