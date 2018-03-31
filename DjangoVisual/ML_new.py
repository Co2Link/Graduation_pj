from sklearn import svm,datasets
import pymongo as pymongo
import random
import re
import numpy as np
from sklearn.feature_selection import SelectKBest,chi2,RFE
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import MinMaxScaler
from operator import itemgetter

class zombie_detection():
    def __init__(self):
        self.CONN=pymongo.MongoClient('localhost',27017)
        self.fans=self.CONN['new_label']['fans']
        data_list=list(self.fans.find())
        self.data_list=random.sample(data_list,len(data_list))
        # self.data_list=data_list
        self.X = [];self.y = []
        for i in self.data_list:
            self.X.append(i)
            self.y.append(i['zombie'])
        X_f = self.feature_extraction(self.X)
        self.X_f = MinMaxScaler().fit_transform(X_f)

    def is_chinese(self,uchar):
        if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
            return True
        else:
            return False
    def feature_extraction(self,raw_feature_list,mask=None):
        result = []
        for raw_feature in raw_feature_list:
            # authentication
            verified_type_1 = 0;
            verified_type_2 = 0;
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
        svc = svm.LinearSVC(class_weight='balanced')
        scores = cross_val_score(svc,X_f, self.y, cv=10, scoring='accuracy')  # 自动应用分层抽样
        mean_score=scores.mean()
        return mean_score
    def feature_selection_filter(self,f_num=None):
        select_bset=SelectKBest(chi2, k=5)
        select_bset.fit(self.X_f, self.y)
        scores_list=select_bset.scores_
        # print(scores_list)
        rank_list=[]
        for i in sorted(scores_list,reverse=True):
            for ii,count in zip(scores_list,range(len(scores_list))):
                if i==ii:
                   rank_list.append(count)

        if f_num:
            return rank_list[:f_num]
        else:
            return rank_list
    def feature_selection_filter_wrapper(self,f_num=None):
        svc=svm.LinearSVC(class_weight='balanced')
        selector=RFE(svc,n_features_to_select=f_num,step=1)
        selector=selector.fit(self.X_f,self.y)
        selected_mask=list(selector.support_)
        return selected_mask


def main():
    zd=zombie_detection()
    best_mask=[0,1,2,3,4,5,11,12,13]
    # zd.cross_validation(best_mask)
    score_list=[]
    for f_num in range(1,15):
        mask=zd.feature_selection_filter(f_num=f_num)
        score_dict = {}
        score_dict['f_num']=f_num
        score_dict['mask']=mask
        score_dict['accuracy']=zd.cross_validation(mask)
        score_list.append(score_dict)
    score_list=sorted(score_list,key=itemgetter('accuracy'),reverse=True)
    print(score_list)

    # score_list=[]
    # for f_num in range(1,15):
    #     mask=zd.feature_selection_filter_wrapper(f_num=f_num)
    #     score_dict = {}
    #     score_dict['f_num']=f_num
    #     score_dict['mask']=mask
    #     score_dict['accuracy']=zd.cross_validation(mask)
    #     score_list.append(score_dict)
    # score_list=sorted(score_list,key=itemgetter('accuracy'),reverse=True)
    # print(score_list)


if __name__ == '__main__':
    main()



