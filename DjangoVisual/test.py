import datetime
import requests
import re
from snownlp import SnowNLP
import pymongo as pymongo
import matplotlib.pyplot as plt
import random

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号



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


def main():
    # bar()
    my_list=[1,2,3]
    print(random.choice(my_list))
    print(random.randint(1,10))
if __name__ == '__main__':
    main()