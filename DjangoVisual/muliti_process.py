from multiprocessing import Process, Queue,Pool
from snownlp import SnowNLP
import os, time, random

# 写数据进程执行的代码:
def write(data_list,q):
    print('Process to write: %s' % os.getpid())
    # for value in ['A', 'B', 'C']:
    #     print('Put %s to queue...' % value)
    #     q.put(value)
    #     time.sleep(random.random())

    for i in data_list:
        print('Put %s to queue...' % i)
        s=SnowNLP(i)
        score=s.sentiments
        if score>0.7:
            q.put({'string':i,'type':'pos'})
        elif score<0.3:
            q.put({'string':i,'type':'neg'})


# 读数据进程执行的代码:
def read(q):
    print('Process to read: %s' % os.getpid())
    f_pos=open('pos.txt','w',encoding='utf-8')
    f_neg=open('neg.txt','w',encoding='utf-8')
    while True:
        i = q.get(True)
        if i['type']=='pos':
            f_pos.write(i['string'])
        elif i['type']=='neg':
            f_neg.write(i['string'])


def int_up(num):
    if num>int(num):
        return int(num)+1
    else:
        return int(num)

def splist(list,s=None,n=None):
    if n:
        s=int_up(len(list)/n)
    return [list[i:i+s] for i in range(len(list)) if i%s==0]

if __name__=='__main__':
    with open('text.txt','r',encoding='utf-8') as f:
        data_list=f.readlines()
        print(len(data_list))

        my_splist=splist(data_list,n=8)

        for i,count in zip(my_splist,range(len(my_splist))):
            print('no. {}: {}'.format(count,len(i)))

        q = Queue()

        pw_list=[]
        for count in range(8):
            pw=Process(target=write,args=(my_splist[count],q))
            pw.start()
            pw_list.append(pw)

        # pw1 = Process(target=write, args=(my_splist[0],q))
        # pw2 = Process(target=write, args=(my_splist[1],q))
        # pw3 = Process(target=write, args=(my_splist[2],q))
        # pw4 = Process(target=write, args=(my_splist[3],q))
        # pw5 = Process(target=write, args=(my_splist[4],q))
        # pw6 = Process(target=write, args=(my_splist[5],q))
        # pw7 = Process(target=write, args=(my_splist[6],q))
        # pw8 = Process(target=write, args=(my_splist[7],q))

        pr = Process(target=read, args=(q,))
        start=time.time()
        pr.start()

        for pw in pw_list:
            pw.join()
        pr.terminate()
        end=time.time()
        print('time cost: {}'.format(str(end-start)))