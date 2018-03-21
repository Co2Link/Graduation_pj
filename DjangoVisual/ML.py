from sklearn import svm,datasets
import pymongo as pymongo
import numpy as np
import random
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
        if raw_feature['verified_type']==-1:    # verified_type
            verified_type=0
        elif raw_feature['verified_type']==0:
            verified_type=0.5
        else:
            verified_type=1
        if raw_feature['description']:
            description=1
        else:
            description=0
        fans_rate=raw_feature['followers_count']/raw_feature['follow_count']
        # fans_rate=(raw_feature['follow_count']+1)/(raw_feature['followers_count']+1)

        result.append([fans_rate,verified_type,description,
                       raw_feature['follow_count'],raw_feature['followers_count'],
                       raw_feature['statuses_count']])
    return result







def main():

    ## para
    tran_rate=0.9
    ##
    CONN=pymongo.MongoClient('localhost',27017)
    col=CONN['new_label']['fans']
    X=[]
    Y=[]
    data=[]
    ## 对取出数据进行乱序处理
    for i in col.find():
        data.append(i)
    data=random.sample(data,len(data))

    for i in data:
        Y.append(i.pop('zombie'))
        X.append(i)

    tran_num=int(tran_rate*len(X))
    print('tran_num: {}'.format(tran_num))
    print('test_num: {}'.format(len(X)-tran_num))

    X=feature_extraction(X)
    X,_,_=autoNorm(X)
    print(np.shape(X))

    svc=svm.SVC(class_weight=[])
    svc.fit(X[:tran_num],Y[:tran_num])
    score=svc.score(X[tran_num:],Y[tran_num:])
    print("accuracy: {}".format(score))

    predict_label=list(svc.predict(X[tran_num:]))
    real_label=Y[tran_num:]
    print('predict_label',predict_label)
    print('real_label   ',real_label)

    count=0
    index_list=[]
    for p,r in zip(predict_label,real_label):
        if p!=r:
            index_list.append(count+tran_num)
        count += 1
    print(index_list)
    print(len(index_list))

    for i in index_list:
        print(data[i]['sid'])






if __name__ == '__main__':
    main()

# #调用SVC()
# clf = svm.SVC()
# #载入鸢尾花数据集
# iris = datasets.load_iris()
# X = iris.data
# print(X)
# print(type(X))
# print(X.shape)
# normDataSet,_,_=autoNorm(X)
# print(normDataSet)
# y = iris.target
# #fit()训练
# clf.fit(X,y)
# #predict()预测
# pre_y = clf.predict(X[5:10])
# print(pre_y)
# print(y[5:10])
# #导入numpy
# import numpy as np
# test = np.array([[5.1,2.9,1.8,3.6]])
# #对test进行预测
# test_y = clf.predict(test)
# print(test_y)