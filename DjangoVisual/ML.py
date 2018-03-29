from sklearn import svm,datasets
import pymongo as pymongo
import numpy as np
import random
import re
import datetime
def autoNorm(dataSet):      ## 将numpy.array归一化
    if not isinstance(dataSet,np.ndarray):
        dataSet=np.array(dataSet)
    minVals=dataSet.min(0)
    maxVals=dataSet.max(0)
    ranges=maxVals-minVals
    m=dataSet.shape[0]
    normDataSet=dataSet-np.tile(minVals,(m,1))
    normDataSet=normDataSet/np.tile(ranges,(m,1))
    return normDataSet,ranges,minVals

def feature_extraction(raw_feature_list):
    result=[]
    for raw_feature in raw_feature_list:
        #authentication
        if raw_feature['verified_type']==-1:    # verified_type
            verified_type=0
        elif raw_feature['verified_type']==0:
            verified_type=1
        elif raw_feature['verified_type']==200:
            verified_type=5
        elif raw_feature['verified_type']==220:
            verified_type=10
        else:
            verified_type=15
        #description
        if raw_feature['description']:
            description=1
        else:
            description=0
        #member
        if raw_feature['mbtype']>2:
            mb=1
        else:
            mb=0
        # fans_rate
        if raw_feature['follow_count']==0:
            raw_feature['follow_count']=1
        fans_rate=raw_feature['followers_count']/raw_feature['follow_count']
        if fans_rate>10:
            fans_rate=10
        #name_has_num
        if re.search(r'\d',raw_feature['screen_name']):
            name_has_num=1
        else:
            name_has_num=0

        result.append([fans_rate,verified_type,mb,
                       raw_feature['follow_count'],raw_feature['followers_count'],
                       raw_feature['statuses_count']])
    return result


def zombie_detection(data,test_list=None,debug=False):
    ## para
    tran_rate=0.9
    ##

    X=[]
    Y=[]
    ## 对取出数据进行乱序处理
    # random.seed(datetime.datetime.now().second)
    if test_list:   #合并 训练集与测试集
        tran_num=len(data)
        data=data+test_list
    else:
        tran_num = int(tran_rate * len(X))
        data=random.sample(data,len(data))

    for i in data:
        Y.append(i.pop('zombie'))
        X.append(i)


    if debug:
        print('tran_num: {}'.format(tran_num))
        print('test_num: {}'.format(len(X)-tran_num))

    X_f=feature_extraction(X)             ###
    X_f,_,_=autoNorm(X_f)

    svc=svm.LinearSVC(class_weight='balanced')
    svc.fit(X_f[:tran_num],Y[:tran_num])
    score=svc.score(X_f[tran_num:],Y[tran_num:])
    if debug:
        print("accuracy: {}".format(score))

    predict_label=list(svc.predict(X_f[tran_num:]))
    real_label=Y[tran_num:]

    return_list=[]

    if debug:
        print('predict_label',predict_label)
        print('real_label   ',real_label)
    p_count=0
    for pre,rea in zip(predict_label,real_label):
        if pre!=rea:
            return_list.append(X[tran_num+p_count]['sid'])
            if debug:
                print('sid: {}, real: {}'.format(X[tran_num+p_count]['sid'],rea))
        p_count+=1


    return score,return_list




def multi_test(data_list):
    ave_score=0
    total_list=[]
    for i in range(1000):
        score,return_list=zombie_detection(data_list)
        ave_score+=score
        total_list+=return_list
        # print(score)

    count_dict={}
    for i in total_list:
        if i not in list(count_dict.keys()):
            count_dict[i]=1
        else:
            count_dict[i]+=1
    print(sorted(count_dict.items(),key=lambda x:x[1]))
    ave_score/=1000
    print(ave_score)

# def unique_test(tran_list,test_list):
#     svc = svm.LinearSVC(class_weight='balanced')
#     tran_num=len(tran_list)
#     data_list=tran_list+test_list
#
#     # X_tran=[]
#     # y_tran=[]
#     # X_test=[]
#     # y_test=[]
#     # for tran,test in zip(tran_list,test_list):
#     #     y_tran.append(tran.pop('zombie'))
#     #     X_tran.append(tran)
#     #     y_test.append(test.pop('zombie'))
#     #     X_test.append(test)
#     # X_tran_f=feature_extraction(X_tran)
#     # X_test_f=feature_extraction(X_test)
#     # X_tran_f,_,_=autoNorm(X_tran_f)
#     # X_test_f,_,_=autoNorm(X_test_f)
#
#     X=[]
#     y=[]
#     for i in data_list:
#         y.append(i.pop('zombie'))
#         X.append(i)
#     X_f=feature_extraction(X)
#     X_f,_,_=autoNorm(X_f)
#
#
#     svc.fit(X_tran_f,y_tran)
#     score=svc.score(X_test_f,y_test)
#     print('score: {}'.format(score))
#
#     for X,y in zip(X_test,y_test):
#
#         if svc.predict(X)!=y:
#             print()


def main():
    CONN=pymongo.MongoClient('localhost',27017)
    fans=CONN['new_label']['fans']
    fans_test=CONN['new_label']['fans_test']
    # print(zombie_detection(list(fans.find()),debug=True))
    # multi_test(list(fans.find()))
    print(zombie_detection(list(fans.find()),list(fans_test.find()),debug=True))



if __name__ == '__main__':
    main()
