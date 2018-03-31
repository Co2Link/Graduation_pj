import  requests
import urllib.request
import datetime
import pymongo
import json
import requests
import re
from sklearn.preprocessing import MinMaxScaler
from matplotlib.dates import drange,date2num
import random
import numpy as np

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
    nine='3279873201'
    a=1880564361
    b=3912883937
    c=5723240588
    e=1740329954

    # my_dict={'a':1,'b':2}
    # my_dict[nine]=1
    # print(my_dict)
    my_array=np.array([1,2,3,4])
    print(my_array[[1,2]])
    print(type(my_array))
    for i in range(1,12):
        print(i)









if __name__=='__main__':
    main()