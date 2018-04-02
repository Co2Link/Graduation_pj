from sklearn import svm,datasets
import pymongo as pymongo
import random
import re
import numpy as np
from sklearn.feature_selection import SelectKBest,chi2,RFE
from sklearn.model_selection import cross_val_score,cross_validate
from sklearn.preprocessing import MinMaxScaler,StandardScaler
from sklearn.externals import joblib
from itertools import combinations
import time
from operator import itemgetter

#1104+600测出来的最佳mask
best_mask=[0, 2, 3, 5, 6, 10, 11]
class zombie_detection():
    def __init__(self,model=None,mask=None):
        #db
        self.CONN=pymongo.MongoClient('localhost',27017)
        self.fans=self.CONN['new_label']['fans']
        data_list=list(self.fans.find())
        ### new
        self.new_fans=self.CONN['new_label']['new_fans']
        data_list+=list(self.new_fans.find())
        ###

        self.data_list=random.sample(data_list,len(data_list))  #乱序
        #分离标签与数据
        self.X = [];self.y = []
        for i in self.data_list:
            self.X.append(i)
            self.y.append(i['zombie'])
        #特征选择
        X_f = self.feature_extraction(self.X,mask)
        self.Scaler=MinMaxScaler().fit(X_f)
        self.X_f = MinMaxScaler().fit_transform(X_f)
        self.Min=self.Scaler.data_min_
        self.Range=self.Scaler.data_range_
        self.mask=mask
        if model:
            self.svc=joblib.load(model)
        else:
            self.svc=svm.LinearSVC(class_weight='balanced')
            # self.svc=svm.SVC(class_weight='balanced')

    def get_model(self,mask=None):
        X_f = self.feature_extraction(self.X,mask)
        scaler=MinMaxScaler()
        X_f = scaler.fit_transform(X_f)
        score_list=cross_val_score(self.svc,X=X_f,y=self.y,cv=10,scoring='accuracy')
        print('mean_score: {}'.format(score_list.mean()))
        self.svc.fit(X=X_f,y=self.y)
        self.mask=mask
        self.Min=scaler.data_min_
        self.Range=scaler.data_range_
        joblib.dump(self.svc,'svc.model')

    def predict(self,people):
        if type(people)==list:
            X_f = self.feature_extraction(people, mask=self.mask)
            X_f = ((np.array(X_f) - self.Min) / self.Range).tolist()
            return self.svc.predict(X_f)
        else:
            X_f=self.feature_extraction([people],mask=self.mask)[0]
            X_f=((np.array(X_f)-self.Min)/self.Range).tolist()
            return self.svc.predict([X_f])[0]


    def is_chinese(self,uchar):
        if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
            return True
        else:
            return False
    def feature_extraction(self,raw_feature_list,mask=None):
        result = []
        for raw_feature in raw_feature_list:
            # authentication
            verified_type_1 = 0
            verified_type_2 = 0
            verified_type_3 = 0
            if raw_feature['verified_type'] == -1:  # verified_type
                verified_type_1 = 1
            elif raw_feature['verified_type'] == 0:
                verified_type_2 = 1
            else:
                verified_type_3 = 1
            # member
            if raw_feature['mbtype'] > 2:
                mb = 1
            else:
                mb = 0
            # fans_rate
            if raw_feature['follow_count'] == 0:
                raw_feature['follow_count'] = 1
            fans_rate = raw_feature['followers_count'] / raw_feature['follow_count']
            if fans_rate > 10:
                fans_rate = 10

            # number_num
            name = raw_feature['screen_name']
            if name=='':
                name='用户'+str(raw_feature['sid'])
            number_num = len(re.findall(r'\d+', name))
            # name_len
            if str(raw_feature['sid']) in name:
                name_len = 7
            else:
                name_len = len(name)
            # num_ratio
            num_ratio = 0
            for i in name:
                if i.isdigit():
                    num_ratio += 1
            num_ratio /= len(name)
            # unique_char_num
            name_set = set()
            for i in name:
                name_set.add(i)
            if str(raw_feature['sid']) in name:
                unique_char_num = 1
            else:
                unique_char_num = len(name_set)
            # name_has_num
            if re.search(r'\d', name) and str(raw_feature['sid']) not in name:
                name_has_num = 1
            else:
                name_has_num = 0
            # mode_1
            if self.is_chinese(name[0]) and name[-1].isdigit() and str(raw_feature['sid']) not in name:
                mode_1 = 1
            else:
                mode_1 = 0
            # description_len
            description_len = len(raw_feature['description'])

            all_feature=[fans_rate,verified_type_1,verified_type_2,verified_type_3,mb,
                           description_len,number_num,name_len,num_ratio,unique_char_num,
                           name_has_num,raw_feature['follow_count'],raw_feature['followers_count'],raw_feature['statuses_count']]

            if mask: #特征选择
                selected_feature =np.array(all_feature)[mask].tolist()
            else:
                selected_feature=all_feature
            result.append(selected_feature)
        return result
    def cross_validation(self,mask=None):
        X_f = self.feature_extraction(self.X,mask)
        X_f = MinMaxScaler().fit_transform(X_f)
        scores = cross_val_score(self.svc,X_f, self.y, cv=10, scoring='accuracy')  # 自动应用分层抽样
        mean_score=scores.mean()
        return mean_score
    def feature_selection_filter(self,f_num=None):
        select_bset=SelectKBest(chi2, k=5)
        select_bset.fit(self.X_f, self.y)
        scores_list=select_bset.scores_
        print(scores_list)
        rank_list=[]
        for i in sorted(scores_list,reverse=True):
            for ii,count in zip(scores_list,range(len(scores_list))):
                if i==ii:
                   rank_list.append(count)

        if f_num:
            return rank_list[:f_num]
        else:
            return rank_list
    def feature_selection_wrapper(self,f_num=None):
        selector=RFE(self.svc,n_features_to_select=f_num,step=1)
        selector=selector.fit(self.X_f,self.y)
        selected_mask=list(selector.support_)
        return selected_mask

    def exhaustion(self):
        # 先用filter过滤掉4个特征
        mask = sorted(self.feature_selection_filter(10))
        print(mask)
        mask_list = []  # 生成所有的组合
        for i in range(10):
            mask_list += list(combinations(mask, i + 1))
        mask_list = [list(i) for i in mask_list]
        print(len(mask_list))
        print(mask_list)
        result_list = []
        start_time = time.time()
        print('start_time: {}'.format(start_time))
        for mask in mask_list:
            result_dict = {}
            result_dict['accuracy'] = self.cross_validation(mask)
            result_dict['mask'] = mask
            result_dict['f_num'] = len(mask)
            result_list.append(result_dict)
            print(result_dict)
        result_list = sorted(result_list, key=itemgetter('accuracy'), reverse=True)
        with open('feature_selection_log_new_600_whole.txt', 'w') as f:
            f.writelines('original_mask: {}\n'.format(str(mask)))
            for i in result_list:
                f.writelines(str(i) + '\n')
        end_time = time.time()
        print('end_time: {}'.format(end_time))
        print('time_cost: {}'.format(end_time - start_time))
        print('best: {}'.format(str(result_list[0])))



def main():
    CONN=pymongo.MongoClient('localhost',27017)

    zd=zombie_detection()

    #特征选择
    # zd.exhaustion()

    #训练并储存模型
    zd.get_model(best_mask)

    #real_test
    count=0
    fans_list=list(CONN['syn_12']['fans_1'].find(filter={'master_id':'1621036195'}))
    print(len(fans_list))
    predict_list=zd.predict(fans_list)
    for i,fans in zip(predict_list,fans_list):
        if i:
            print(fans['sid'])
            count+=1
    print(count)

    #test old_zombie
    # count = 0
    # test_num=1000
    # fans_list=random.sample(list(fans.find()),test_num)
    # predict_list=zd.predict(fans_list)
    # for pre,rea in zip(predict_list,fans_list):
    #     if pre==rea['zombie']:
    #         count+=1
    # print(count/test_num)


    #test new_zombie
    # count=0
    # fans_list=list(new_zombie.find())
    # predict_list=zd.predict(fans_list)
    # for pre,rea in zip(predict_list,fans_list):
    #     if pre==rea['zombie']:
    #         count+=1
    # print(count/len(predict_list))


    # new
    # count=0
    # fans_1=CONN['syn_12']['fans_1']
    # fans_list=list(fans_1.find(filter={'master_id':'3065368482'}))
    # predict_list=zd.predict(fans_list)
    # for i in predict_list:
    #     if i :
    #         count+=1
    # print(count/len(predict_list))
    # print(len(predict_list))


if __name__ == '__main__':
    main()



