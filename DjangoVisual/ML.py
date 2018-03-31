from sklearn import svm,datasets
import pymongo as pymongo
import numpy as np
import random
import re
from sklearn.feature_selection import SelectKBest,chi2,RFE
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import MinMaxScaler
import datetime

def is_chinese(uchar):
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False

def get_data():
    CONN=pymongo.MongoClient('localhost',27017)
    fans=CONN['new_label']['fans']
    X=[];y=[]
    for i in fans.find():
        X.append(i)
        y.append(i['zombie'])
    X_f=feature_extraction(X)
    X_f=MinMaxScaler().fit_transform(X_f).tolist()
    return X_f,y


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
        verified_type_1=0;verified_type_2=0;verified_type_3=0
        if raw_feature['verified_type']==-1 :    # verified_type
            verified_type_1=1
        elif raw_feature['verified_type']==0:
            verified_type_2=1
        else:
            verified_type_3=1

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

        #number_num
        name = raw_feature['screen_name']
        number_num=len(re.findall(r'\d+',name))

        #name_len
        if str(raw_feature['sid'])in name:
            name_len=7
        else:
            name_len=len(name)

        #num_ratio
        num_ratio=0
        for i in name:
            if i.isdigit():
                num_ratio+=1
        num_ratio/=len(name)

        #unique_char_num
        name_set=set()
        for i in name:
            name_set.add(i)
        if str(raw_feature['sid']) in name:
            unique_char_num=1
        else:
            unique_char_num=len(name_set)

        #name_has_num
        if re.search(r'\d',name) and str(raw_feature['sid']) not in name:
            name_has_num=1
        else:
            name_has_num=0

        #mode_1
        if is_chinese(name[0])and name[-1].isdigit() and str(raw_feature['sid']) not in name:
            mode_1=1
        else:
            mode_1=0

        #description_len    #good
        description_len=len(raw_feature['description'])

        # print(raw_feature)
        # print(number_num,name_len,num_ratio,unique_char_num,name_has_num)

        # result.append([fans_rate,verified_type_1,verified_type_2,verified_type_3,mb,description_len,number_num,
        #                name_len,num_ratio,unique_char_num,name_has_num,raw_feature['follow_count'],
        #                raw_feature['followers_count'],raw_feature['statuses_count']])
        # result.append([raw_feature['follow_count'],name_has_num,verified_type,num_ratio,fans_rate,mb,number_num,description_len,raw_feature['statuses_count'],unique_char_num])
        result.append([fans_rate,verified_type_1,verified_type_2,verified_type_3,mb,description_len,
                       raw_feature['follow_count'],
                       raw_feature['followers_count'],raw_feature['statuses_count']])

        # result.append([fans_rate,description_len,num_ratio,name_has_num,raw_feature['follow_count']])
        #wrapper_6
        # result.append([fans_rate,description_len,num_ratio,unique_char_num,raw_feature['follow_count'],
        #                raw_feature['followers_count']])
    return result



def zombie_detection(data,test_list=None,debug=False):
    ## para
    tran_rate=0.9
    ##

    X=[]
    Y=[]
    ## 对取出数据进行乱序处理
    if test_list:   #合并 训练集与测试集
        tran_num=len(data)
        data=data+test_list
    else:
        tran_num = int(tran_rate * len(data))
        data=random.sample(data,len(data))

    for i in data:
        Y.append(i['zombie'])
        X.append(i)

    if debug:
        print('tran_num: {}'.format(tran_num))
        print('test_num: {}'.format(len(X)-tran_num))

    X_f=feature_extraction(X)             ###
    X_f=MinMaxScaler().fit_transform(X_f)

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

def feature_selection(data_list):
    X=[]
    y=[]
    for i in data_list:
        y.append(i['zombie'])
        X.append(i)
    X_f=feature_extraction(X)
    X_f,_,_=autoNorm(X_f)
    X_f=np.array(X_f)
    my_selection=SelectKBest(chi2,k=2)
    X_new=my_selection.fit_transform(X_f,y)
    scores_list=my_selection.scores_
    print('scores_list: {}'.format(scores_list))
    rank_list=[]
    for i in sorted(scores_list,reverse=True):
        count=0
        for ii in scores_list:
            count+=1
            if i==ii:
                rank_list.append(count)
    print('rank_list: {}'.format(rank_list))

def feature_selection_wrapper(data_list):
    X=[]
    y=[]
    for i in data_list:
        y.append(i['zombie'])
        X.append(i)
    X_f=feature_extraction(X)
    X_f,_,_=autoNorm(X_f)
    X_f=np.array(X_f)
    svc=svm.LinearSVC(class_weight='balanced')
    rfe=RFE(estimator=svc,n_features_to_select=6,step=2)
    rfe.fit(X_f,y)
    print(rfe.ranking_)
    print(rfe.support_)

def feature_selection_model(data_list):
    pass

def cross_validation(data_list):
    svc=svm.LinearSVC(class_weight='balanced')

def main():
    CONN=pymongo.MongoClient('localhost',27017)
    fans=CONN['new_label']['fans']
    fans_test=CONN['new_label']['fans_test']
    data_list=list(fans.find())
    # print(zombie_detection(list(fans.find()),debug=True))
    multi_test(list(fans.find()))
    # print(zombie_detection(list(fans.find()),list(fans_test.find()),debug=True))

    # feature_selection(data_list)

    # feature_selection_wrapper(data_list)




if __name__ == '__main__':
    main()
