from snownlp import sentiment
from multiprocessing import Pool
from .my_wordcloud import dealHtmlTags
from collections import Iterable
import time


s = sentiment.Sentiment()
s.load('D:/Python/Graduation_pj/DjangoVisual/Visual/ass/sentiment.marshal')
def write_new(data_list):
    # print('Process to write: %s' % os.getpid())
    ret_list=[]
    for i in data_list:
        score=s.classify(i)
        ret_list.append({'string':i,'score':score})
    return ret_list

def int_up(num):
    if num>int(num):
        return int(num)+1
    else:
        return int(num)

def splist(list,s=None,n=None,Iterable=False):
    if n:
        s=int_up(len(list)/n)
    if Iterable:
        return (list[i:i + s] for i in range(len(list)) if i % s == 0)
    else:
        return [list[i:i + s] for i in range(len(list)) if i % s == 0]

def sentiment_multiprocess(data_list,thread_num=7):
    print('data_list len: {}'.format(len(data_list)))
    my_splist = splist(data_list, n=thread_num)
    pool = Pool(processes=thread_num)
    process_list=[]
    start=time.time()
    for list in my_splist:
        process_list.append(pool.apply_async(func=write_new,args=(list,)))
    pool.close()
    pool.join()
    end=time.time()
    result_list=[]
    for i in process_list:
        result_list.extend(i.get())
    print('time cost: {}'.format(str(end-start)))
    return result_list

def sentiment_single(sent):
    sent=sent.split('//')[0] #去掉转发内容，若只有转发内容，则取转发内容，若为多重转发，则取最近的转发内容
    return s.classify(dealHtmlTags(sent))

def new_multi_process(data_list,thread_num=7):
    start=time.time()
    my_splist = splist(data_list,n=thread_num,Iterable=True)
    pool = Pool(processes=thread_num)
    ret_list=pool.map(write_new,my_splist)
    end=time.time()
    # print('sample: {}'.format(str(result_list[0])))
    # print('len of result list: {}'.format(len(result_list)))
    print('time cost: {}'.format(str(end-start)))
    return ret_list
def main():
    with open('E:/data/buf/' + 'neg_test.txt', 'r', encoding='utf-8') as f:
        data_list=f.readlines()
        print('len of data_list: {}'.format(len(data_list)))
        sentiment_multiprocess(data_list)


if __name__ == '__main__':
    main()


