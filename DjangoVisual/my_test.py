import  requests
import urllib.request
import datetime
import pymongo
import json
from matplotlib.dates import drange,date2num

def clean():
    result=requests.get(url='http://127.0.0.1:8000/api/clean/')
    print(result.text)
def crawl(id):
    result=requests.post(url='http://127.0.0.1:8000/api/crawl/', data={"id":id})
    print(result.text)


def check_user_exist_and_esttimate_time(id,time_dict):
    time=0
    result=requests.get(url='https://m.weibo.cn/api/container/getIndex?containerid=100505{}'.format(id))
    try:
        userInfo=json.loads(result.text)['data']['userInfo']
        followers_count=userInfo['followers_count']
        statuses_count=userInfo['statuses_count']
    except Exception as e:
        return 0
    #calculate time
    if followers_count/20>250:
        time+=250+250*19*3
    else:
        time+=followers_count/18
    if statuses_count/10>10:
        time+=10
    else:
        time+=statuses_count/10
    time_dict['time']=time/220
    return True

def main():
    # clean()
    nine=3279873201
    a=1880564361
    b=3912883937
    c=5723240588
    e=1740329954
    time_dict={}
    if check_user_exist_and_esttimate_time('3279873201',time_dict):
        print(time_dict)
    else:
        print('fuck')






if __name__=='__main__':
    main()