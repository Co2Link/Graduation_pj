import  requests
import urllib.request
import datetime
from matplotlib.dates import drange,date2num

def clean():
    result=requests.get(url='http://127.0.0.1:8000/api/clean/')
    print(result.text)
def crawl(id):
    result=requests.post(url='http://127.0.0.1:8000/api/crawl/', data={"id":id})
    print(result.text)



def main():
    # clean()
    nine=3279873201
    a=1880564361
    b=3912883937
    c=5723240588
    e=1740329954
    # crawl(e)
    # if 0 and 1 or 0:
    #     print('fuck')
    # d1=datetime.datetime.strptime('2015-6-1', '%Y-%m-%d')
    # d2=datetime.datetime.strptime('2015-11-1', '%Y-%m-%d')
    # d3=date2num(d2)
    # print(d3)
    # print(d1.timestamp()/86400)
    # ddelta=datetime.timedelta(days=10)
    # dates=drange(d1,d2,ddelta)
    # print(dates)
    # url='https://wx4.sinaimg.cn/orj480/70172289ly8fmnmkfz173j20qo0qogo8.jpg'
    # response = urllib.request.urlopen(url=url)
    # buf=response.read()
    # with open('cat_500_600.jpg', 'wb') as f:
    #     f.write(buf)
    print(second=datetime.datetime().now().second)





if __name__=='__main__':
    main()