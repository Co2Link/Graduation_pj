import  requests
import urllib.request
import datetime
from matplotlib.dates import drange,date2num
import pymongo
import json
import random
def clean():
    result=requests.get(url='http://127.0.0.1:8000/api/clean/')
    print(result.text)
def crawl(id):
    result=requests.post(url='http://127.0.0.1:8000/api/crawl/', data={"id":id})
    print(result.text)

def create_new_db():
    CONN=pymongo.MongoClient('localhost',27017)
    col_prefix='fans_2_{}'
    col=CONN['syn_11']['fans_2']
    new_col_1=CONN['label'][col_prefix.format(1)]
    new_col_2 = CONN['label'][col_prefix.format(2)]
    new_col_3 = CONN['label'][col_prefix.format(3)]
    new_col_4 = CONN['label'][col_prefix.format(4)]
    new_col_list=[new_col_1,new_col_2,new_col_3,new_col_4]

    data=list(col.aggregate([{'$sample': {'size': 1000}}]))
    data_list=[]
    for i in range(1,5):
        data_list.append(data[(i-1)*200:i*200])
    for (col,data) in zip(new_col_list,data_list):
        col.create_index([('sid',pymongo.ASCENDING)])
        col.insert_many(data)

def add_fied():
    CONN=pymongo.MongoClient('localhost',27017)
    new_col_list=[CONN['label']['fans_1_1'],CONN['label']['fans_1_2']
        ,CONN['label']['fans_1_3'],CONN['label']['fans_1_4'],
        CONN['label']['fans_2_1'],CONN['label']['fans_2_2']
        ,CONN['label']['fans_2_3'],CONN['label']['fans_2_4']]
    for col in new_col_list:
        for i in col.find():
            col.find_one_and_update({'sid':i['sid']},{'$set':{'zombie':0}})

def combine(col_name):
    CONN = pymongo.MongoClient('localhost', 27017)
    fans=CONN['new_label']['fans']
    fans_=CONN['new_label'][col_name]
    count=0
    for i in fans_.find():
        if not fans.find_one(filter={'sid':i['sid']}):
            result_1 = requests.get(
                url='https://m.weibo.cn/api/container/getIndex?containerid=100505{}'.format(i['sid']))
            result_2 = requests.get(
                url='https://m.weibo.cn/api/container/getIndex?containerid=230283{}_-_INFO'.format(i['sid']))

            try:
                cards = json.loads(result_2.text)['data']['cards']
                location = '其他'
                for card in cards:
                    if 'card_group' in card:
                        for sub_card in card['card_group']:
                            if 'item_name' in sub_card and sub_card['item_name'] == '所在地':
                                location = sub_card['item_content']

                userInfo = json.loads(result_1.text)['data']['userInfo']
                sid = i['sid']
                my_dict = {}
                # my_dict['master_id'] = i['master_id']
                my_dict['sid'] = sid
                my_dict['follow_count'] = userInfo['follow_count']
                my_dict['followers_count'] = userInfo['followers_count']
                my_dict['statuses_count'] = userInfo['statuses_count']
                my_dict['verified_type'] = userInfo['verified_type']
                my_dict['description'] = userInfo['description']
                my_dict['mbrank'] = userInfo['mbrank']
                my_dict['mbtype'] = userInfo['mbtype']
                my_dict['screen_name'] = userInfo['screen_name']
                my_dict['location'] = location
                my_dict['zombie'] = i['zombie']

                fans.insert_one(my_dict)
                count+=1
            except Exception as e:
                print(e)
                print(result_1.text)
                print(i['sid'])
                continue
    print(count)



def update():
    CONN = pymongo.MongoClient('localhost', 27017)
    fans=CONN['new_label']['fans_test']
    for i in fans.find():
        result_1 = requests.get(url='https://m.weibo.cn/api/container/getIndex?containerid=100505{}'.format(i['sid']))
        result_2=requests.get(url='https://m.weibo.cn/api/container/getIndex?containerid=230283{}_-_INFO'.format(i['sid']))



        try:

            cards = json.loads(result_2.text)['data']['cards']
            location='其他'
            for card in cards:
                if 'card_group' in card:
                    for sub_card in card['card_group']:
                        if 'item_name' in sub_card and sub_card['item_name'] == '所在地':
                            location = sub_card['item_content']

            userInfo = json.loads(result_1.text)['data']['userInfo']
            sid=i['sid']
            my_dict={}
            my_dict['sid']=sid
            my_dict['follow_count']=userInfo['follow_count']
            my_dict['followers_count']=userInfo['followers_count']
            my_dict['statuses_count']=userInfo['statuses_count']
            my_dict['verified_type']=userInfo['verified_type']
            my_dict['description']=userInfo['description']
            my_dict['mbrank']=userInfo['mbrank']
            my_dict['mbtype']=userInfo['mbtype']
            my_dict['screen_name']=userInfo['screen_name']
            my_dict['location']=location
            my_dict['zombie']=i['zombie']

            fans.find_one_and_replace(filter={'sid':sid},replacement=my_dict)
        except Exception as e:
            print(e)
            print(result_1.text)
            print(i['sid'])
            continue




def crawl_mbrank():
    CONN=pymongo.MongoClient('localhost',27017)
    col=CONN['new_label']['fans']
    count=0
    for i in col.find():
        if not 'mbrank' in i or not 'mbtype' in i:
            count+=1
            result = requests.get(url='https://m.weibo.cn/api/container/getIndex?containerid=100505{}'.format(i['sid']))
            try:
                userInfo=json.loads(result.text)['data']['userInfo']
                col.find_one_and_update(filter={'sid': i['sid']},
                                        update={'$set': {'mbrank': userInfo['mbrank'], 'mbtype': userInfo['mbtype']}})

            except Exception as e:
                print(result.text)
                print(i['sid'])
                if '用户不存在' in result.text:
                    col.find_one_and_delete(filter={'sid':i['sid']})
                    print("id: {} 不存在,已删除".format(i['sid']))
    print(count)


def add_test_data():
    CONN=pymongo.MongoClient('localhost',27017)
    fans_test=CONN['new_label']['fans_test']
    fans_test.create_index([('sid',pymongo.ASCENDING)])





def main():
    CONN=pymongo.MongoClient('localhost',27017)
    fans=CONN['new_label']['fans']
    fans_test=CONN['new_label']['fans_test']
    for i in fans_test.find():
        fans.insert_one(i)















if __name__=='__main__':
    main()