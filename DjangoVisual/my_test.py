import  requests
import urllib.request
import datetime
import pymongo
import json
import requests
from matplotlib.dates import drange,date2num
import random

def clean():
    result=requests.get(url='http://127.0.0.1:8000/api/clean/')
    print(result.text)
def crawl(id):
    result=requests.post(url='http://127.0.0.1:8000/api/crawl/', data={"id":id})
    print(result.text)

def add_description():
    CONN=pymongo.MongoClient('localhost',27017)
    new_col=CONN['new_label']['fans']
    str_list=[]
    valid_list=[]
    for i in new_col.find():
        str_list.append(i['descriptiodn'])
        if not i['description']:
            valid_list.append(i['description'])
    print(str_list)
    print(len(str_list))
    print(len(valid_list))


def main():
    # clean()
    nine=3279873201
    a=1880564361
    b=3912883937
    c=5723240588
    e=1740329954

    list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    slice = random.sample(list, len(list))  # 从list中随机获取5个元素，作为一个片断返回
    print(slice)
    print(list)










if __name__=='__main__':
    main()