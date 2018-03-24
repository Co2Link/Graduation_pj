import pymongo as pymongo
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def ana_description(data_list):
    print(col.find().count())
    print(len(data_list))
    aa = 0
    ab = 0
    ba = 0
    bb = 0
    for i in data_list:

        if i['zombie']:
            if i['description']:
                aa += 1
            else:
                ab += 1
        else:
            if i['description']:
                ba += 1
            else:
                bb += 1
    print(aa)
    print(ab)
    print(ba)
    print(bb)

def ana_fo_foer(data_list):
    zombie_list=[]
    normal_list=[]
    folloers_couont_ave=0
    follow_count_ave=0
    for i in data_list:
        folloers_couont_ave+=i['followers_count']
        follow_count_ave+=i['follow_count']
    folloers_couont_ave/=len(data_list)
    follow_count_ave/=len(data_list)
    print('follower: {}'.format(folloers_couont_ave))
    print('follow: {}'.format(follow_count_ave))

    count_zombie=0
    count_normal=0

    for i in data_list:
        if i['zombie']==1 and i['followers_count']<2*folloers_couont_ave and i['follow_count']<4*follow_count_ave:
            zombie_list.append(i)
            count_zombie+=1
        elif i['zombie']==0 and i['followers_count']<2*folloers_couont_ave and i['follow_count']<4*follow_count_ave:
            normal_list.append(i)
            count_normal+=1

    plt.plot([i['follow_count'] for i in zombie_list],[i['followers_count'] for i in zombie_list],'ko',label='zombie')
    plt.plot([i['follow_count'] for i in normal_list],[i['followers_count'] for i in normal_list],'b.',label='normal')
    plt.xlabel('关注数')
    plt.ylabel('粉丝数')
    print('zombie: {}'.format(count_zombie))
    print('normal: {}'.format(count_normal))
    plt.legend()
    plt.show()




def main():
    CONN = pymongo.MongoClient('localhost', 27017)
    col = CONN['new_label']['fans']

    data_list = list(col.find())

    count=0
    for i in data_list:
        if i['follow_count']>1000 and not i['zombie']:
            print(i['sid'])
            count+=1
    print(count)


    ana_fo_foer(data_list)

if __name__ == '__main__':
    main()
