import scrapy
import json
import logging
class fans_spider(scrapy.Spider):
    name='fans'
    def __init__(self,*args,**kwargs):
        super(fans_spider,self).__init__(*args,**kwargs)
        self.fans_urls='https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{}&since_id={}'
        self.user_urls='https://m.weibo.cn/api/container/getIndex?containerid=100505{}'
        self.id=kwargs.get('id')
    def start_requests(self):
        url=self.user_urls.format(self.id)
        yield scrapy.Request(url=url)
    def parse(self, response):
        result=json.loads(response.text)['data']
        try:
            fans_num=result['userInfo']['followers_count']
        except KeyError as e:
            print(e)
        logging.debug(fans_num)

