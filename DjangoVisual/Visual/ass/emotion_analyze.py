from snownlp import sentiment
from multiprocessing import Pool
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

def splist(list,s=None,n=None):
    if n:
        s=int_up(len(list)/n)
    return [list[i:i+s] for i in range(len(list)) if i%s==0]

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
    return s.classify(sent)


