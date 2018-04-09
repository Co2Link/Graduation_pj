import pymongo
import requests
import random
import numpy as np
from sklearn.externals import joblib

def is_chinese(uchar):
    if uchar >= u'\u4e00' and uchar <= u'\u9fff':
        return True
    else:
        return False

def clean():
    result=requests.get(url='http://127.0.0.1:8000/api/clean/')
    print(result.text)
def crawl(id):
    result=requests.post(url='http://127.0.0.1:8000/api/crawl/', data={"id":id})
    print(result.text)

def add_description():
    CONN=pymongo.MongoClient('localhost',27017)
    fans_1=CONN['syn_12']['fans_1']

    new_zombie=CONN['label']['new_zombie']


    new_zombie.create_index([('sid',pymongo.ASCENDING)],unique=True)
    data_list=list(fans_1.find(filter={'master_id':3065368482}))
    random_list=random.sample(data_list,600)
    new_zombie.insert_many(random_list)





def int_up(num):
    if num>int(num):
        return int(num)+1
    else:
        return int(num)
def main():
    # CONN=pymongo.MongoClient('localhost',27017)
    # fans_1=CONN['syn_12']['fans_1']
    #
    # new_zombie=CONN['label']['new_zombie']


    # new_zombie.create_index([('sid',pymongo.ASCENDING)],unique=True)
    # data_list=list(fans_1.find(filter={'master_id':'3065368482'}))
    # random_list=random.sample(data_list,600)
    # new_zombie.insert_many(random_list)

    print(int_up(3))










if __name__=='__main__':
    main()