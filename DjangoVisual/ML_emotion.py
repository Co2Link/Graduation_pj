from multiprocessing import Process, Queue,Pool
from snownlp import SnowNLP,sentiment
import os, time, random

ODpath='E:/data/buf/'

# 写数据进程执行的代码:
def write_new(data_list):
    # print('Process to write: %s' % os.getpid())
    ret_list=[]
    s = sentiment.Sentiment()
    s.load(fname=ODpath + 'sentiment.marshal')
    # s.load()
    for i in data_list:
        score=s.classify(i)
        ret_list.append({'string':i,'score':score})
    return ret_list


# 读数据进程执行的代码:

def int_up(num):
    if num>int(num):
        return int(num)+1
    else:
        return int(num)

def splist(list,s=None,n=None):
    if n:
        s=int_up(len(list)/n)
    return [list[i:i+s] for i in range(len(list)) if i%s==0]

def sentiment_multiprocess(data_list,thread_num=8):
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

def cov2unicode(path,sourceEncoding):
    with open(path,'r',encoding=sourceEncoding) as f:
        buf=f.read()
    with open(path,'w',encoding='utf-8') as f:
        f.write(buf)

def div_set(ratio):
    with open(ODpath+'neg60000.txt','r',encoding='gbk') as f_neg,open(ODpath+'pos60000.txt','r',encoding='gbk')as f_pos:
        pos_list=f_pos.readlines()
        neg_list=f_neg.readlines()
        pos_tran=random.sample(pos_list,int(len(pos_list)*ratio))
        neg_tran=random.sample(neg_list,int(len(neg_list)*ratio))
        pos_test=list(set(pos_list)^set(pos_tran))
        neg_test=list(set(neg_list)^set(neg_tran))
        with open(ODpath+'pos_tran.txt','w',encoding='utf-8') as pt:
            pt.writelines(pos_tran)
        with open(ODpath+'pos_test.txt','w',encoding='utf-8') as pt:
            pt.writelines(pos_test)
        with open(ODpath+'neg_tran.txt','w',encoding='utf-8') as pt:
            pt.writelines(neg_tran)
        with open(ODpath+'neg_test.txt','w',encoding='utf-8') as pt:
            pt.writelines(neg_test)



def train():
    start=time.time()
    sentiment.train(ODpath+'neg_tran.txt',ODpath+'pos_tran.txt')
    sentiment.save(ODpath+'sentiment.marshal')
    end=time.time()
    print('train time cost: {}'.format(str(end-start)))

def test():
    with open(ODpath+'neg_test.txt','r',encoding='utf-8') as f_1 ,open(ODpath+'pos_test.txt','r',encoding='utf=8') as f_2:
        start=time.time()
        result_list_pos=sentiment_multiprocess(f_2.readlines())
        result_list_neg=sentiment_multiprocess(f_1.readlines())
        count_pos=0
        count_neg=0
        print(len(result_list_neg))
        print(len(result_list_pos))
        for pos,neg in zip(result_list_pos,result_list_neg):
            if pos['score']>0.5:
                count_pos+=1
            if neg['score']<0.5:
                count_neg+=1
        end=time.time()
        print('pos_acr: {}'.format(str(count_pos/len(result_list_pos))))
        print('neg_acr: {}'.format(str(count_neg/len(result_list_neg))))
        print('test time cost: {}'.format(str(end-start)))




if __name__=='__main__':

    start=time.time()
    div_set(ratio=0.9)
    train()
    test()
    end=time.time()
    print('total time cost: {}'.format(str(end-start)))
    # with open(r'D:\Anaconda2\envs\py3\envs\graduation_pj\Lib\site-packages\snownlp\normal\stopwords.txt','r',encoding='utf-8') as f:
    #     for i in f.readlines():
    #         print(i)
    # my_str='#一毛钱的浪漫#我同学的男朋友在刚跟她谈恋爱的时候，找了她出生的那年的一毛钱硬币，然后一直磨，磨成图片的样子，还专门把1993那里留了下来。――别人的男朋友真好[泪]  via@Gemini???'
    # print(SnowNLP(my_str).words)



