import pymongo as pymongo
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

CONN=pymongo.MongoClient('localhost',27017)
db=CONN['syn_4']

# user=db['user']
# fans_1=db['fans_1']
# fans_2=db['fans_2']
# post=db['post']

def gender(id):
    fans_1 = db['fans_1']
    labels = ['男', '女']
    result_m = fans_1.find(filter={'gender': 'm','master_id':id})
    result_f = fans_1.find(filter={'gender': 'f','master_id':id})
    sizes = [result_m.count(), result_f.count()]
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=False)
    plt.savefig(fname='D:/Python/Graduation_pj/DjangoVisual/static/images/gender')
    plt.show()

def fans_fans_num(id):
    fans_1=db['fans_1']
    num_list=[]
    result=fans_1.find(filter={"master_id":id})
    for i in result:
        # if i['followers_count']==178552579 or i['followers_count']==508029:
        #     continue
        num_list.append(i['followers_count'])
    count_dict={'0-100':0,'100-1k':0,'1k-10k':0,'10k-100k':0,'大于100k':0}
    print('len:',len(num_list))
    print(num_list)
    for i in num_list:
        if i>=0 and i<100:
            count_dict['0-100']+=1
        elif i>=100 and i<1000:
            count_dict['100-1k']+=1
        elif i>=1000 and i<10000:
            count_dict['1k-10k']+=1
        elif i>=10000 and i<100000:
            count_dict['10k-100k']+=1
        elif i>=100000:
            count_dict['大于100k']+=1
    print(count_dict)


    # n, bins, patches = plt.hist(x=count_dict,density=False, facecolor='g', alpha=0.75)  #alpha 颜色深度
    # n, bins, patches = pl|t.hist(x=x,bins=10,facecolor='g', alpha=0.75)
    label=['0-100','100-1k','1k-10k','10k-100k','大于100k']
    height=[count_dict[i] for i in label]
    plt.bar(x=[1,2,3,4,5],height=height,tick_label=label,visable=True)
    plt.grid(True)
    plt.show()

def main():
    id='3597829674'
    # # gender('3597829674')
    fans_fans_num(id)


    # import numpy as np
    # import matplotlib.pyplot as plt
    #
    # # Fixing random state for reproducibility
    # np.random.seed(19680801)
    #
    # mu, sigma = 100, 15
    # x = mu + sigma * np.random.randn(10000)
    # print(type(x))
    # print(x)
    # print(x.shape)
    #
    # # the histogram of the data
    # n, bins, patches = plt.hist(x=x, bins=20, density=True, facecolor='g', alpha=0.75)  #alpha 颜色深度
    # # n, bins, patches = plt.hist(x=x,bins=10,facecolor='g', alpha=0.75)
    #
    # plt.xlabel('Smarts')
    # plt.ylabel('Probability')
    # plt.title('Histogram of IQ')
    # plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
    # plt.axis([40, 160, 0, 0.03])
    # plt.grid(True)
    # plt.show()


if __name__=='__main__':
    main()




