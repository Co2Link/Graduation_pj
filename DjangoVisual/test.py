import datetime
import requests
import re
from snownlp import SnowNLP
import pymongo as pymongo

def one():
    return [1,2,3],3

def clean_text(text):
    text=re.sub(pattern=r'\\"',repl='"',string=text)
    return text



def main():
    CONN=pymongo.MongoClient('localhost',27017)
    col=CONN['mongodb_test_1']['post']
    post=col.find_one({'id':123})
    text=r"马上飞回国啦！跟老美一起high了几天，挑战了美国南部最大的pizza，25km/h的跑步机，等等等等等，后面慢慢剪出来！<span class=\"url-icon\"><img src=\"//h5.sinaimg.cn/m/emoticon/icon/others/d_doge-d903433c82.png\" style=\"width:1em;height:1em;\" alt=\"[doge]\"></span><span class=\"url-icon\"><img src=\"//h5.sinaimg.cn/m/emoticon/icon/others/d_doge-d903433c82.png\" style=\"width:1em;height:1em;\" alt=\"[doge]\"></span><span class=\"url-icon\"><img src=\"//h5.sinaimg.cn/m/emoticon/icon/others/d_doge-d903433c82.png\" style=\"width:1em;height:1em;\" alt=\"[doge]\"></span> <a data-url=\"http://t.cn/RqzrF15\" href=\"http://weibo.com/p/1001018000117031000000005\" data-hide=\"\"><span class=\"url-icon\"><img src=\"https://h5.sinaimg.cn/upload/2015/09/25/3/timeline_card_small_location_default.png\"></span></i><span class=\"surl-text\">美国·芝加哥</a> ​"
    print(text)
    print(clean_text(text))
if __name__ == '__main__':
    main()