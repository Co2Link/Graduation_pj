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

def combine():
    CONN = pymongo.MongoClient('localhost', 27017)
    fans=CONN['new_label']['fans']
    fans_2=CONN['new_label']['fans_2']
    origin=CONN['syn_11']['fans_2']
    for i in fans_2.find():
        doc=origin.find_one(filter={'sid':i['sid']})
        doc['zombie']=i['zombie']
        fans.insert(doc)


def crawl_mbrank():
    CONN=pymongo.MongoClient('localhost',27017)
    col=CONN['new_label']['fans']
    for i in col.find():
        if not 'mbrank' in i:
            result = requests.get(url='https://m.weibo.cn/api/container/getIndex?containerid=100505{}'.format(i['sid']))
            col.find_one_and_update(filter={'sid':i['sid']},update={'$set':{'mbrank':json.loads(result.text)['data']['userInfo']['mbrank']}})



def main():
    # clean()
    nine=3279873201
    a=1880564361
    b=3912883937
    c=5723240588
    e=1740329954
    combine()










if __name__=='__main__':
    main()