import pymongo
import requests
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
    svc=joblib.load('svc.model')
    svc.score()










if __name__=='__main__':
    main()