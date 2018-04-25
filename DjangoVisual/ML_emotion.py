from multiprocessing import Process, Queue,Pool
from snownlp import SnowNLP,sentiment
import time, random,re

from sklearn.model_selection import train_test_split
ODpath='E:/data/buf/9/'
TDpath='E:/data/buf/train/'

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

def clean_post(sent):
    result=re.sub('回复.+?:','',sent)
    ret=re.sub('@[^ :：]+','',result)
    ret=re.sub(r'http:[a-zA-Z0-9/._]*','',ret)
    return ret

def div_set(ratio):
    with open(TDpath+'neg60000.txt','r',encoding='gbk') as f_neg,open(TDpath+'pos60000.txt','r',encoding='gbk')as f_pos:
        pos_list=f_pos.readlines()
        neg_list=f_neg.readlines()
        print(neg_list[20])
        print(neg_list[20].split('//'))

        #去掉转发内容
        new_pos_list=[]
        new_neg_list=[]
        for p in pos_list:
            sp=p.split('//')
            if not sp[0] or sp[0]==' ' or sp[0]=='转': #没有内容
                clean_sent=p
            else:
                clean_sent=sp[0].strip()+'\n'
            clean_sent=clean_post(clean_sent).strip()+'\n'
            if clean_sent=='\n':                #有内容 但为@的内容
                new_pos_list.append(p)
            else:
                new_pos_list.append(clean_sent)
        for p in neg_list:
            sp=p.split('//')
            if not sp[0] or sp[0]==' ' or sp[0]=='转':
                clean_sent=p
            else:
                clean_sent=sp[0].strip()+'\n'
            clean_sent=clean_post(clean_sent).strip()+'\n'
            if clean_sent=='\n':
                new_neg_list.append(p)
            else:
                new_neg_list.append(clean_sent)

        #去掉@名字；回复
        new_pos_list=[clean_post(i).strip()+'\n' for i in new_pos_list]
        new_neg_list=[clean_post(i).strip()+'\n' for i in new_neg_list]

        need_ret=1
        if not need_ret:
            pass
        else:
            new_pos_list = [clean_post(i).strip() + '\n' for i in pos_list]
            new_neg_list = [clean_post(i).strip() + '\n' for i in neg_list]

        # new_neg_list=neg_list
        # new_pos_list=pos_list

        #debug
        with open(ODpath+'new_neg.txt','w',encoding='utf-8') as pt:
            pt.writelines(new_neg_list)
        with open(ODpath+'new_pos.txt','w',encoding='utf-8') as pt:
            pt.writelines(new_pos_list)

        random.seed(10)
        pos_tran=random.sample(new_pos_list,int(len(new_pos_list)*ratio))
        neg_tran=random.sample(new_neg_list,int(len(new_neg_list)*ratio))
        pos_test=list(set(new_pos_list)^set(pos_tran))
        neg_test=list(set(new_neg_list)^set(neg_tran))
        print('pos_tran: {}'.format(len(pos_tran)))
        print('neg_tran: {}'.format(len(neg_tran)))
        print('pos_test: {}'.format(len(pos_test)))
        print('neg_tes: {}'.format(len(neg_test)))
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
    div_set(0.9)
    train()
    test()



