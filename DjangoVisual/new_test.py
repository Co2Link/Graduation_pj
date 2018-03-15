import  requests
import urllib.request
import datetime
from matplotlib.dates import drange,date2num
import pymongo
import random
def clean():
    result=requests.get(url='http://127.0.0.1:8000/api/clean/')
    print(result.text)
def crawl(id):
    result=requests.post(url='http://127.0.0.1:8000/api/crawl/', data={"id":id})
    print(result.text)

def create_new_db():
    CONN=pymongo.MongoClient('localhost',27017)
    col=CONN['syn_10']['fans_1']
    new_col_1=CONN['label']['fans_1_1']
    new_col_2 = CONN['label']['fans_1_2']
    new_col_3 = CONN['label']['fans_1_3']
    new_col_4 = CONN['label']['fans_1_4']
    new_col_list=[CONN['label']['fans_1_1'],CONN['label']['fans_1_2']
        ,CONN['label']['fans_1_3'],CONN['label']['fans_1_4']]

    data=list(col.aggregate([{'$sample': {'size': 2000}}]))
    data_list=[]
    for i in range(1,5):
        data_list.append(data[(i-1)*500:i*500])
    for (col,data) in zip(new_col_list,data_list):
        col.create_index([('sid',pymongo.ASCENDING)])
        col.insert_many(data)

def add_fied():
    CONN=pymongo.MongoClient('localhost',27017)
    new_col_list=[CONN['label']['fans_1_1'],CONN['label']['fans_1_2']
        ,CONN['label']['fans_1_3'],CONN['label']['fans_1_4']]
    for col in new_col_list:
        for i in col.find():
            col.find_one_and_update({'sid':i['sid']},{'$set':{'zombie':0}})





def main():
    # clean()
    nine=3279873201
    a=1880564361
    b=3912883937
    c=5723240588
    e=1740329954

    # create_new_db()
    #
    # add_fied()
    random.seed(datetime.datetime.now().second)
    print(random.randint(100000,999999))




if __name__=='__main__':
    main()