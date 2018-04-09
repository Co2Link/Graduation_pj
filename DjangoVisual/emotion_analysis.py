from snownlp import SnowNLP
from multiprocessing import Process,Queue,Pool
import time
from snownlp.normal import filter_stop
import jieba

# my_str=u'回复@南极JaronNan:I have other shows so I cannot continue on the #saythewordstour# . But @曲婉婷Wanting a tour lasts until the end of March in North America ! Go see it !//@南极JaronNan:So that means your show has come to an end so far?'
# s = SnowNLP(my_str)
#
# split_list=s.words         # [u'这个', u'东西', u'真心',
#                 #  u'很', u'赞']
# print(s.sentiments)
# print(split_list)
# print(filter_stop(split_list))
pos_list=[]
pos_count=0
neg_list=[]
neg_count=0
count=0

def write2txt(q):
    with open('pos.txt','w') as f:
        while True:
            my_str = q.get(True)
            f.write(my_str+'\n')


def my_sentiment(my_str,q):
    count=0

    for i in my_str:
        count += 1
        print(count)
        s = SnowNLP(i)
        score = s.sentiments
        if score > 0.7:
            q.put(my_str)
    time.sleep(1)
    q.close()
    # if type(my_str)==list:
    #     for i in my_str:
    #         count+=1
    #         print(count)
    #         s = SnowNLP(i)
    #         score = s.sentiments
    #         if score > 0.7:
    #             q.put(my_str)
    # else:
    #     s = SnowNLP(my_str)
    #     score = s.sentiments
    #     if score > 0.7:
    #         q.put(my_str)




def main():
    with open(r'text.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        data_list = lines[:1000]
        q = Queue()
        start = time.time()

        p1 = Process(target=my_sentiment, args=(data_list[:int(len(data_list) / 2)], q))
        p2 = Process(target=my_sentiment, args=(data_list[int(len(data_list) / 2):], q))
        pw=Process(target=write2txt,args=(q,))

        p1.start()
        p2.start()
        pw.start()

        p1.join()
        p2.join()
        pw.terminate()
        # for i in lines[:1000]:
        #     count+=1

        end = time.time()
        print('time cost: {}'.format(str(end - start)))

if __name__ == '__main__':
    main()