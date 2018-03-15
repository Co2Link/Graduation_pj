import pymongo as pymongo
import matplotlib
matplotlib.use('Agg')       #解决matplotlib存储图像在django中应用的问题
import matplotlib.pyplot as plt
import datetime
from matplotlib.dates import DateFormatter
import pandas as pd
import urllib.request

### matplotlib画图

class create_pic():
    def __init__(self,id):
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        self.CONN = pymongo.MongoClient('localhost', 27017)
        self.db = self.CONN['syn_10']
        self.id=str(id)
    def __del__(self):
        self.CONN.close()
    def get_pic(self):
        user=self.db['user'].find_one(filter={'id':self.id})
        with urllib.request.urlopen(url=user['avatar_hd']) as response:  # 必须关闭连接
            buf = response.read()
        with open('D:/Python/Graduation_pj/DjangoVisual/static/images/user.jpg', 'wb') as f:
            f.write(buf)

    def gender(self):
        fans_1 = self.db['fans_1']
        labels = ['男', '女']
        result_m = fans_1.find(filter={'gender': 'm', 'master_id': self.id})
        result_f = fans_1.find(filter={'gender': 'f', 'master_id': self.id})
        sizes = [result_m.count(), result_f.count()]
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=False)
        plt.legend()
        plt.savefig(fname='D:/Python/Graduation_pj/DjangoVisual/static/images/gender')
        plt.close()
        # plt.show()

    def anti_zombie(self,result_list):  # 返回完整的表，与只含僵尸的表
        complete_list = []
        dirty_list = []
        clean_list = []
        for i in result_list:
            complete_list.append(i)
            if i['statuses_count'] == 0 or i['followers_count'] < i['follow_count'] / 10 and i['follow_count'] > 100:
                dirty_list.append(i)
            else:
                clean_list.append(i)
        return [complete_list, dirty_list, clean_list]

    def multi_bar(self,result_list):  # 为每个list画一个bar
        count = 0  # 区分两个列表，一个完整，一个僵尸
        for dif_list in result_list:
            count += 1
            num_list = []
            for i in dif_list:
                num_list.append(i['followers_count'])
            count_dict = {'0-100': 0, '100-1k': 0, '1k-10k': 0, '10k-100k': 0, '大于100k': 0}
            for i in num_list:
                if i >= 0 and i < 100:
                    count_dict['0-100'] += 1
                elif i >= 100 and i < 1000:
                    count_dict['100-1k'] += 1
                elif i >= 1000 and i < 10000:
                    count_dict['1k-10k'] += 1
                elif i >= 10000 and i < 100000:
                    count_dict['10k-100k'] += 1
                elif i >= 100000:
                    count_dict['大于100k'] += 1
            tick_label = ['0-100', '100-1k', '1k-10k', '10k-100k', '大于100k']
            height = [count_dict[i] for i in tick_label]
            if count == 1:
                label = 'normal'
            else:
                label = 'zombie'
            container = plt.bar(x=[1, 2, 3, 4, 5], height=height, tick_label=tick_label, label=label)
            for i in container:
                cor = (i.get_x() + i.get_width() / 2, i.get_height())
                if count == 1:
                    plt.text(cor[0], cor[1], '%.0f' % cor[1], ha='center', va='bottom', fontsize=11)
                else:
                    plt.text(cor[0], 0, '%.0f' % cor[1], ha='center', va='bottom', fontsize=11)
        plt.legend()
        plt.savefig(fname='D:\Python\Graduation_pj\DjangoVisual\static\images\dfans_num')
        plt.close()
        # plt.show()

    def fans_num(self):
        fans_1 = self.db['fans_1']
        result = fans_1.find(filter={"master_id": self.id})
        self.multi_bar(self.anti_zombie(result)[:2])

    def post_freq(self):
        post = self.db['post']
        result = post.find(filter={'author_id': int(self.id)})
        post_dict = {}
        for i in result:  # 统计频率
            date = i['created_at']
            if date in post_dict:
                post_dict[date] += 1
            else:
                post_dict[date] = 1
        post_list = []
        for key, value in post_dict.items():  # 转为list， 并且转为datetime
            post_list.append({'created_at': datetime.datetime.strptime(key, '%Y-%m-%d'), 'time': value})
        new_post_list = sorted(post_list, key=lambda post: post['created_at'])  # 排序
        # print(new_post_list)
        max_time = new_post_list[-1]['created_at']
        pad_post_list = []  # 填充
        for i in range(10):  # 从最近一天起，取10天
            current_time = max_time - datetime.timedelta(days=i)
            pad_post_list.append({'created_at': current_time, 'time': 0})
            for old_time in new_post_list:
                if current_time == old_time['created_at']:
                    pad_post_list[i] = (old_time)
        pad_post_list = pad_post_list[::-1]  # 反转
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))  # 设置时间显示格式，否则只能显示年份
        plt.plot_date(x=[post['created_at'] for post in pad_post_list], y=[post['time'] for post in pad_post_list],
                      fmt='r')
        plt.xticks(pd.date_range(start=pad_post_list[0]['created_at'], end=pad_post_list[-1]['created_at'], freq='2D'),
                   rotation=30)  # 设置时间间隔
        plt.savefig(fname='D:\Python\Graduation_pj\DjangoVisual\static\images\post_freq')
        plt.close()
        # plt.show()

    def fans_authen(self):
        fans_1 = self.db['fans_1']
        cursor = fans_1.find(filter={'master_id': self.id})
        cursor = self.anti_zombie(cursor)[2]
        verified_dict = {}
        for i in cursor:
            if i['verified_type'] in verified_dict:
                verified_dict[i['verified_type']] += 1
            else:
                verified_dict[i['verified_type']] = 1
        name_verified_dict = {}
        for key, value in verified_dict.items():
            if key == -1:
                name_verified_dict['普通'] = verified_dict[key]
            elif key == 200:
                name_verified_dict['初级达人'] = verified_dict[key]
            elif key == 220:
                name_verified_dict['高级达人'] = verified_dict[key]
            elif key == 0:
                name_verified_dict['黄V'] = verified_dict[key]
            else:
                if '蓝V' in name_verified_dict:
                    name_verified_dict['蓝V'] += verified_dict[key]
                else:
                    name_verified_dict['蓝V'] = verified_dict[key]
        x_list = []
        label_list = []
        for key, value in name_verified_dict.items():
            x_list.append(value)
            label_list.append(key)
        plt.pie(x=x_list, labels=label_list, autopct='%1.1f%%', shadow=False)
        plt.legend()
        plt.savefig(fname='D:\Python\Graduation_pj\DjangoVisual\static\images\dfans_authen')
        plt.close()

CONN=pymongo.MongoClient('localhost',27017)
db=CONN['syn_9']

def get_pic(url):
    with urllib.request.urlopen(url=url) as response:   #必须关闭连接
        buf=response.read()
    with open('D:/Python/Graduation_pj/DjangoVisual/static/images/user.jpg', 'wb') as f:
        f.write(buf)


def gender(id):
    id=str(id)
    fans_1 = db['fans_1']
    labels = ['男', '女']
    result_m = fans_1.find(filter={'gender': 'm','master_id':id})
    result_f = fans_1.find(filter={'gender': 'f','master_id':id})
    sizes = [result_m.count(), result_f.count()]
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=False)
    plt.legend()
    plt.savefig(fname='D:/Python/Graduation_pj/DjangoVisual/static/images/gender')
    plt.close()
    # plt.show()

def anti_zombie(result_list):   #返回完整的表，与只含僵尸的表
    complete_list=[]
    dirty_list=[]
    clean_list=[]
    for i in result_list:
        complete_list.append(i)
        if i['statuses_count']==0 or i['followers_count']<i['follow_count']/10 and i['follow_count']>100:
            dirty_list.append(i)
        else:
            clean_list.append(i)
    return [complete_list,dirty_list,clean_list]
def multi_bar(result_list): #   为每个list画一个bar
    count=0 #区分两个列表，一个完整，一个僵尸
    for dif_list in result_list:
        count+=1
        num_list = []
        for i in dif_list:
            num_list.append(i['followers_count'])
        count_dict={'0-100':0,'100-1k':0,'1k-10k':0,'10k-100k':0,'大于100k':0}
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
        tick_label=['0-100','100-1k','1k-10k','10k-100k','大于100k']
        height=[count_dict[i] for i in tick_label]
        if count==1:
            label='normal'
        else:
            label='zombie'
        container=plt.bar(x=[1,2,3,4,5],height=height,tick_label=tick_label,label=label)
        for i in container:
            cor = (i.get_x() + i.get_width() / 2, i.get_height())
            if count==1:
                plt.text(cor[0], cor[1], '%.0f' % cor[1], ha='center', va='bottom', fontsize=11)
            else:
                plt.text(cor[0], 0, '%.0f' % cor[1], ha='center', va='bottom', fontsize=11)
    plt.legend()
    plt.savefig(fname='D:\Python\Graduation_pj\DjangoVisual\static\images\dfans_num')
    plt.close()
    # plt.show()

def fans_num(id):
    id=str(id)
    fans_1=db['fans_1']
    result=fans_1.find(filter={"master_id":id})
    multi_bar(anti_zombie(result)[:2])

def post_freq(id):
    id=int(id)
    post=db['post']
    result=post.find(filter={'author_id':id})
    post_dict={}
    for i in result:    #统计频率
        date=i['created_at']
        if date in post_dict:
            post_dict[date]+=1
        else:
            post_dict[date]=1
    post_list=[]
    for key,value in post_dict.items(): #转为list， 并且转为datetime
        post_list.append({'created_at':datetime.datetime.strptime(key,'%Y-%m-%d'),'time':value})
    new_post_list=sorted(post_list,key=lambda post:post['created_at'])          #排序
    max_time=new_post_list[-1]['created_at']
    pad_post_list=[]                                    #  填充
    for i in range(10):#从最近一天起，取10天
        current_time=max_time-datetime.timedelta(days=i)
        pad_post_list.append({'created_at':current_time,'time':0})
        for old_time in new_post_list:
            if current_time==old_time['created_at']:
                pad_post_list[i]=(old_time)
    pad_post_list=pad_post_list[::-1]                #反转
    fig=plt.figure()
    ax=fig.add_subplot(1,1,1)
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d')) #设置时间显示格式，否则只能显示年份
    plt.plot_date(x=[post['created_at'] for post in pad_post_list], y=[post['time'] for post in pad_post_list], fmt='r')
    plt.xticks(pd.date_range(start=pad_post_list[0]['created_at'],end=pad_post_list[-1]['created_at'],freq='2D'),rotation=30)   #设置时间间隔
    plt.savefig(fname='D:\Python\Graduation_pj\DjangoVisual\static\images\post_freq')
    plt.close()
    # plt.show()

def fans_authen(id):
    id=str(id)
    fans_1=db['fans_1']
    cursor=fans_1.find(filter={'master_id':id})
    cursor=anti_zombie(cursor)[2]
    verified_dict={}
    for i in cursor:
        if i['verified_type'] in verified_dict:
            verified_dict[i['verified_type']]+=1
        else:
            verified_dict[i['verified_type']]=1
    # print(verified_dict)
    name_verified_dict={}
    for key,value in verified_dict.items():
        if key==-1:
            name_verified_dict['普通']=verified_dict[key]
        elif key==200:
            name_verified_dict['初级达人']=verified_dict[key]
        elif key==220:
            name_verified_dict['高级达人']=verified_dict[key]
        elif key==0:
            name_verified_dict['黄V']=verified_dict[key]
        else:
            if '蓝V' in name_verified_dict:
                name_verified_dict['蓝V']+=verified_dict[key]
            else:
                name_verified_dict['蓝V']=verified_dict[key]
    # print(name_verified_dict)
    x_list=[]
    label_list=[]
    for key,value in name_verified_dict.items():
        x_list.append(value)
        label_list.append(key)
    plt.pie(x=x_list,labels=label_list,autopct='%1.1f%%', shadow=False)
    plt.legend()
    plt.savefig(fname='D:\Python\Graduation_pj\DjangoVisual\static\images\dfans_authen')
    plt.close()

def main():
    nine=3279873201
    a=1880564361
    b=3912883937
    c=5723240588
    # # gender('3597829674')
    # fans_num(str(nine))
    w=create_pic(b)
    w.post_freq()

if __name__=='__main__':
    main()




