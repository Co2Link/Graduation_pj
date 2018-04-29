import datetime
import requests
import re,time
from snownlp import SnowNLP,sentiment,seg
import pymongo as pymongo
import matplotlib.pyplot as plt
import random,jieba
from html.parser import HTMLParser
import math

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

ODpath='E:/data/buf/'

def bar():
    height=[2.97,3.13,3.4,3.61,3.76]
    tick_label=['2016年Q3','2016年Q4','2017年Q1','2017年Q2','2017年Q3']
    container=plt.bar(x=[1, 2, 3, 4, 5], height=height,width=0.3, tick_label=tick_label,color='gray')
    for i in container:
        cor = (i.get_x() + i.get_width() / 2, i.get_height())
        plt.text(cor[0], cor[1], '%.1f' % cor[1], ha='center', va='bottom', fontsize=11)
    plt.ylabel('微博月活跃人数（单位：亿）')
    plt.xlabel('季度')
    plt.savefig('pic/微博月活跃人数')
    plt.show()
    # plt.savefig(fname='D:\Python\Graduation_pj\DjangoVisual\static\images\dfans_num')
    # plt.close()
def my_db_exit():
    CONN=pymongo.MongoClient('localhost',27017)
    db_label=CONN['label']
    fans_1=list(db_label['fans_1_1'].find())+list(db_label['fans_1_2'].find())+list(db_label['fans_1_3'].find())+list(db_label['fans_1_4'].find())
    fans_2=list(db_label['fans_2_1'].find())+list(db_label['fans_2_2'].find())+list(db_label['fans_2_3'].find())+list(db_label['fans_2_4'].find())

    count_fans_1=0
    count_fans_2=0
    for f_1,f_2 in zip(fans_1,fans_2):
        if f_1['master_id']=="2842266491":
            count_fans_1+=1
        if f_2['master_id']=="2842266491":
            count_fans_2+=1
    print(count_fans_1)
    print(count_fans_2)
def my_test():
    CONN=pymongo.MongoClient('localhost',27017)
    fans=CONN['new_label']['fans']
    Count=0
    for i in list(fans.find()):
        print(i['sid'])
        or_fans=CONN['label']['fans_1'].find_one(filter={'sid':i['sid']})
        if or_fans==None:
            continue
        fans.find_one_and_update(filter={'sid':or_fans['sid']},update={'$set':{'master_id':or_fans['master_id']}})
        Count+=1
    print(Count)
def test_2():
    my_list=[{'p':0.743,'r':0.923},
             {'p': 0.724, 'r': 0.905},
             {'p': 0.712, 'r': 0.902},
             {'p': 0.686, 'r': 0.783},
             {'p': 0.756, 'r': 0.909}]
    my_list_12=[{'p':0.735,'r':0.892},
             {'p': 0.743, 'r': 0.876},
             {'p': 0.738, 'r': 0.888},
             {'p': 0.714, 'r': 0.789},
             {'p': 0.769, 'r': 0.889}]

    my_list_k=[{'p':0.752,'r':0.914},
             {'p': 0.705, 'r': 0.902},
             {'p': 0.654, 'r': 0.864},
             {'p': 0.581, 'r': 0.803},
             {'p': 0.712, 'r': 0.851}]
    my_list_e=[{'p':0.735,'r':0.856},
             {'p': 0.724, 'r': 0.894},
             {'p': 0.701,'r': 0.882},
             {'p': 0.686, 'r': 0.783},
             {'p': 0.760, 'r': 0.840}]




    ave=0
    for i in my_list:
        f=cal(i['p'],i['r'])
        print(f)
        ave+=f
    print(round(ave/len(my_list),3))

def train():
    start=time.time()
    sentiment.train(ODpath+'neg_tran.txt',ODpath+'pos_tran.txt')
    sentiment.save(ODpath+'sentiment.marshal')
    end=time.time()
    print('train time cost: {}'.format(str(end-start)))

def test_NB():
    my_s=sentiment.Sentiment()

    start=time.time()
    my_s.train()
    end=time.time()
    print('time cost: {}'.format(end-start))

def take_first(sent):
    return re.split('//',sent)

def clean_post(sent):
    result=re.sub('回复.+?:','',sent)
    ret=re.sub('@[^ :：]+','',result)
    ret=re.sub(r'http:[a-zA-Z0-9/._]*','',ret)
    return ret

def main():
    sent="@沁姐_想要见?锅求正能量 嘉定//@人类无法阻止的蛋蛋花: 污染到一定程度了~~//@ReleaseM:都僵成这样啦//@小小小小小呆妞: [衰]//@jincarrey: 擦 //@人见人爱赵火火:我靠??//@小阿妮不是小胖纸是大光明: 哎呀妈呀…"


    print(clean_post(sent))
    # print(jiebaclearText(sent))

    # bar()
    # CONN=pymongo.MongoClient('localhost',27017)
    # post=CONN['syn_12']['post']
    #
    # my_str=post.find_one(filter={'id':"3655040005157437"})['text']
    #
    # stopwords_path = 'D:/Python/Graduation_pj/DjangoVisual/Visual/ass/wordcloud_file/stopwords1893.txt'  # 停用词词表
    #
    #
    # my_s=sentiment.Sentiment()
    # my_str='我愛你'
    # my_str=dealHtmlTags(my_str)
    # print(my_str)
    # print(jieba.lcut(my_str))
    # print(seg.seg(my_str))
    # print(jiebaclearText(my_str,stopwords_path))
    # print(my_s.handle(my_str))


def jiebaclearText(text):
    mywordlist = []
    jieba.add_word('[委屈]')
    seg_list = jieba.cut(text, cut_all=False)
    liststr="/ ".join(seg_list)
    with open("D:/Python/Graduation_pj/DjangoVisual/Visual/ass/wordcloud_file/stopwords1893.txt",'r',encoding='utf-8') as f:
        f_stop_seg_list = f.readlines()
        f_stop_seg_list = [i.strip() for i in f_stop_seg_list]
    for myword in liststr.split('/'):
        if not(myword.strip() in f_stop_seg_list):
            mywordlist.append(myword.strip())
    clean_word_list=[]
    my_word_list_del=['网页','微博','链接','全文','回复','转发']
    for i in mywordlist:
        if not i.strip() in my_word_list_del:
            clean_word_list.append(i)
    return clean_word_list
def dealHtmlTags(html):
    '''''
    去掉html标签
    '''
    html=html.strip()
    html=html.strip("\n")
    result=[]
    parse=HTMLParser()
    parse.handle_data=result.append
    parse.feed(html)
    parse.close()
    return "".join(result)

def my_New(pos_Len,neg_len,pos_acc,neg_acc):

    pos_c=pos_Len*pos_acc
    neg_c=neg_len*neg_acc

    A=(pos_c+neg_c)/(pos_Len+neg_len)
    P=pos_c/(pos_c+(neg_len-neg_c))
    R=pos_c/(pos_c+(pos_Len-pos_c))
    F=2*P*R/(P+R)

    print(round(A,3),round(P,3),round(R,3),round(F,3))

if __name__ == '__main__':
    #2
    # pos_Len = 5435
    # neg_len = 5549
    #
    # pos_acc = 0.865317387
    # neg_acc = 0.852225626
    #1
    pos_Len = 5910
    neg_len = 5952

    pos_acc = 0.90287648
    neg_acc = 0.91767473

    #3
    pos_Len = 5910
    neg_len = 5952

    pos_acc = 0.8844331641285956
    neg_acc = 0.9164986559139785
    #
    pos_Len = 5435
    neg_len = 5549

    pos_acc = 0.8507819687212511
    neg_acc = 0.8558298792575239
    my_dict={'a':1,'b':2}


    my_sen=sentiment.Sentiment()
    my_sen.load(fname="D:/Python/Graduation_pj/DjangoVisual/Visual/ass/sentiment.marshal")
    my_str='我爱你啊 我爱你'
    print(my_sen.handle(my_str))
    kk=my_sen.classify(my_str)
    print(kk)
    # main()

