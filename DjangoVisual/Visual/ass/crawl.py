import requests
import re
import json
import datetime
import pymongo as pymongo
CONN=pymongo.MongoClient('localhost',27017)
post=CONN['syn_12']['post']
comments=CONN['syn_12']['comments']

def main():
    pass

def datetime_fmt(datetime_str):
    return str(datetime.datetime.strptime(datetime_str, '%a %b %d %H:%M:%S %z %Y').date())

def crawl_weibo(id):
    result=requests.get(url='https://m.weibo.cn/status/{}'.format(id))
    search_str_list=['attitudes_count','comments_count','reposts_count','created_at']
    post_dict={}
    for search_str in search_str_list:
        search_result = re.findall(r'"{}": (.+),'.format(search_str), result.text)  #在转发
        if search_result:
            if search_str=='created_at':
                post_dict[search_str]=datetime_fmt(search_result[0][1:-1]) #去掉头尾的双引号
            else:
                if 'retweeted_status' in result.text:   #转发的微博中，本微博的信息在第二个位置
                    post_dict[search_str]=search_result[1]
                else:
                    post_dict[search_str]=search_result[0]
        else:
            return 0
    searchobj = re.search(r'"{}": "(.+)",'.format('text'), result.text)
    post_dict['text']=searchobj.group(1)
    searchobj=re.search(r'"retweeted_status".+"text": "(.+)",.+"textLength"', result.text,re.DOTALL)
    if searchobj:
        post_dict['retweeted_status']=True
        post_dict['retweeted_text']=searchobj.group(1)
    else:
        post_dict['retweeted_status'] = False

    #db
    post_dict['id']=str(id)
    try:
        post.insert_one(post_dict)
    except pymongo.errors.DuplicateKeyError as e:
        pass
    post_dict.pop('_id')  # 向mongodb插入后，会多出'_id'键,在此去除该键
    return post_dict

def check_user_exist(id):
    result=requests.get(url='https://m.weibo.cn/api/container/getIndex?containerid=230283{}_-_INFO'.format(id))
    cards = json.loads(result.text)['data']['cards']
    # print(len(cards))
    for card in cards:
        if 'card_group' in card:
            for sub_card in card['card_group']:
                if 'item_name' in sub_card and sub_card['item_name'] == '所在地':
                    return True
    return False





def main():

    print(crawl_weibo(4227895498905169))
    pass

if __name__ == '__main__':
    main()