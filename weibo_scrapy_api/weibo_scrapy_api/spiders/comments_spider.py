import scrapy
import json
import logging
from ..items import comment_Item
class fans_spider(scrapy.Spider):
    name='comments'
    def __init__(self,*args,**kwargs):
        super(fans_spider,self).__init__(*args,**kwargs)
        self.comments_urls='https://m.weibo.cn/api/comments/show?id={}&page={}'   #fans
        self.id=kwargs.get('id')

    def start_requests(self):
        yield scrapy.Request(url=self.comments_urls.format(self.id,1))
        # for page in range(1,11):                                              #每个用户固定爬10页微博
        #     yield scrapy.Request(url=self.post_urls.format(self.id, self.id,page),callback=self.parse_post)
    def parse(self,response):   #info_urls   先获取user的所在地与注册时间
        max_page=json.loads(response.text)['data']['max']
        logging.debug(('max',max_page))
        for i in range(max_page):
            yield scrapy.Request(url=self.comments_urls.format(self.id,i+1),callback=self.parse_page,dont_filter=True)
    def parse_page(self,response):
        page=json.loads(response.text)['data']['data']
        item=comment_Item()
        item['page']=page
        item['post_id']=self.id
        yield item