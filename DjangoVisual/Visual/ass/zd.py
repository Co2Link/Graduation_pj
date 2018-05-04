from sklearn import svm
import pymongo as pymongo
import random
import re,datetime
import numpy as np
from sklearn.feature_selection import SelectKBest,chi2,RFE
from sklearn.model_selection import cross_val_score,cross_validate,train_test_split
from sklearn.preprocessing import MinMaxScaler,StandardScaler
from sklearn.externals import joblib
from itertools import combinations
import time
from operator import itemgetter

#1104+600测出来的最佳mask
best_mask=[0, 2, 3, 4, 5, 6, 10, 11,14]
# best_mask=[0, 2, 3, 4, 5, 6, 10, 11, 13]
# best_mask=[0, 2, 5, 13]
class zombie_detection():
    def __init__(self,model=None,mask=None):
        #db
        self.CONN=pymongo.MongoClient('localhost',27017)
        self.fans=self.CONN['new_label']['fans']
        data_list=list(self.fans.find())
        ### new
        self.new_fans=self.CONN['new_label']['new_fans']
        random.seed(200)
        data_list+=random.sample(list(self.new_fans.find()),150)
        ###

        # self.data_list=random.sample(data_list,len(data_list))  #乱序
        #分离标签与数据
        self.X = [];self.y = []
        for i in data_list:
            self.X.append(i)
            self.y.append(i['zombie'])

        #划分数据集
        self.X_train,self.X_test,self.y_train,self.y_test=train_test_split(self.X,self.y,test_size=0.1,random_state=30)
        self.X_T,self.X_V,self.y_T,self.y_V=train_test_split(self.X_train,self.y_train,test_size=0.1,random_state=30)

        #特征抽取
        X_f = self.feature_extraction(self.X_train,mask)
        self.Scaler=MinMaxScaler().fit(X_f)
        self.X_f = MinMaxScaler().fit_transform(X_f)    #归一化
        self.Min=self.Scaler.data_min_
        self.Range=self.Scaler.data_range_
        self.mask=mask
        self.total_f_num=14
        if model:
            self.svc=joblib.load(model)
        else:
            self.svc=svm.LinearSVC()
    def get_model(self,mask=None,model_name='svc.model'):
        X_f = self.feature_extraction(self.X_T,mask)
        scaler=MinMaxScaler()
        X_f = scaler.fit_transform(X_f)     # 归一化

        self.svc.fit(X=X_f,y=self.y_T)
        self.mask=mask
        self.Min=scaler.data_min_
        self.Range=scaler.data_range_
        joblib.dump(self.svc,model_name)
        #Validation
        correct_count = 0
        for pre,rea in zip(self.predict(self.X_V),self.y_V):
            if pre==rea:
                correct_count+=1
        val_rate=correct_count/len(self.y_V)
        print('validation correct rate: {}'.format(str(val_rate)))

        mean_score=self.cross_validation(mask=self.mask)
        #test
        correct_count=0
        TP=0;FP=0;FN=0
        for pre,rea in zip(self.predict(self.X_test),self.y_test):
            if pre==rea:
                correct_count+=1
                if pre==1:
                    TP+=1
            elif rea==1:
                FP+=1
            elif rea==0:
                FN+=1
        test_rate=correct_count/len(self.y_test)
        P=TP/(TP+FP)
        R=TP/(TP+FN)
        F=2*P*R/(P+R)
        print('test correct rate: {}'.format(str(test_rate)))
        #train
        correct_count=0
        for pre,rea in zip(self.predict(self.X_T),self.y_T):
            if pre==rea:
                correct_count+=1
        train_rate=correct_count/len(self.y_T)
        print('train correct rate: {}'.format(str(train_rate)))

        return {'test':round(test_rate,3),'val':round(mean_score,3),'train':round(train_rate,3),'P':round(P,3),'R':round(R,3),'F':round(F,3)}
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
    def feature_extraction(self,raw_feature_list,mask=None):    #输入：原始用户数据字典
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

            #followers_num_spec
            if raw_feature['followers_count']<10:
                folowers_num_spec=1
            else:
                folowers_num_spec=0


            # number_num
            name = raw_feature['screen_name']
            if name=='':
                name='用户'+str(raw_feature['sid'])
            number_num = len(re.findall(r'\d+', name))
            # name_len
            if str(raw_feature['sid']) in name:
                name_len = 5
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
                           name_has_num,raw_feature['follow_count'],raw_feature['followers_count'],raw_feature['statuses_count'],folowers_num_spec]

            if mask: #特征选择
                selected_feature =np.array(all_feature)[mask].tolist()
            else:
                selected_feature=all_feature
            result.append(selected_feature)
        return result
    def cross_validation(self,mask=None):
        X_f = self.feature_extraction(self.X_train,mask)
        X_f = MinMaxScaler().fit_transform(X_f)
        scores = cross_val_score(self.svc,X_f, self.y_train, cv=5, scoring='accuracy')  # 自动应用分层抽样
        mean_score=scores.mean()
        return mean_score
    def feature_selection_filter(self,f_num=None):
        select_bset=SelectKBest(chi2, k=5)
        select_bset.fit(self.X_f, self.y_train)
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
    def feature_selection_wrapper(self,f_num=None):
        selector=RFE(self.svc,n_features_to_select=f_num,step=1)
        selector=selector.fit(self.X_f,self.y_train)
        selected_mask=list(selector.support_)
        selected_mask=np.array([i for i in range(14)])[selected_mask].tolist()   #由boolean mask 转换为 数字 mask
        return selected_mask
    def exhaustion(self):
        # 先用filter过滤掉4个特征
        mask = sorted(self.feature_selection_filter(10))
        # mask=[i for i in range(13)]
        # print(mask)
        mask_list = []  # 生成所有的组合
        for i in range(10):
            mask_list += list(combinations(mask, i + 1))
        mask_list = [list(i) for i in mask_list]
        # print(len(mask_list))
        # print(mask_list)
        result_list = []
        start_time = time.time()
        for mask in mask_list:
            result_dict = {}
            result_dict['accuracy'] = self.cross_validation(mask)
            result_dict['mask'] = mask
            result_dict['f_num'] = len(mask)
            result_list.append(result_dict)
            # print(result_dict)
        result_list = sorted(result_list, key=itemgetter('accuracy'), reverse=True)
        with open('feature_selection_log_1.txt', 'w') as f:
            f.writelines('time: {}\n'.format(str(datetime.datetime.now())))
            f.writelines('original_mask: {}\n'.format(str(mask)))
            for i in result_list:
                f.writelines(str(i) + '\n')
        end_time = time.time()
        print('time_cost: {}'.format(end_time - start_time))
        print('best: {}'.format(str(result_list[0])))
        return result_list[0]['mask']



def main():
    # test_1()
    # test_2()


    # mask=zd.exhaustion()
    re_list=[]
    for i in range(1):
        zd = zombie_detection()
        re_list.append(zd.get_model(mask=best_mask,model_name='svc.model'))
    test=0
    val=0
    train=0
    P=0
    R=0
    F=0
    for i in re_list:
        test+=i['test']
        val+=i['val']
        train+=i['train']
        P+=i['P']
        R+=i["R"]
        F+=i['F']
    print('test: {}'.format(test/len(re_list)))
    print('val: {}'.format(val/len(re_list)))
    print('train: {}'.format(train/len(re_list)))
    print('P: {}'.format(P/len(re_list)))
    print('R: {}'.format(R/len(re_list)))
    print('F: {}'.format(F/len(re_list)))

    # print(zd.get_model(mask=best_mask,model_name='svc.model'))




    #特征选择
    # zd.exhaustion()

    #训练并储存模型
    # zd.get_model(best_mask)
    #
    # #real_test
    # count=0
    # fans_list=list(CONN['syn_12']['fans_1'].find(filter={'master_id':'1621036195'}))
    # print(len(fans_list))
    # predict_list=zd.predict(fans_list)
    # for i,fans in zip(predict_list,fans_list):
    #     if i:
    #         print(fans['sid'])
    #         count+=1
    # print(count)

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
    count=0
    zd=zombie_detection(r'D:\Python\Graduation_pj\DjangoVisual\Visual\ass\svc.model',best_mask)
    new_zombie=pymongo.MongoClient('localhost',27017)['new_label']['new_fans']
    fans_list=list(new_zombie.find())
    predict_list=zd.predict(fans_list)
    for pre,rea in zip(predict_list,fans_list):
        if pre==rea['zombie']:
            count+=1
            new_zombie.find_one_and_update(filter={'sid':rea['sid']},update={'$set':{'predict':True}})
        else:
            new_zombie.find_one_and_update(filter={'sid':rea['sid']},update={'$set':{'predict':False}})
            print(rea['sid'])
    print(count/len(predict_list))


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


def test_1():
    for i in range(5):
        print('-{}-'.format(i))
        zd = zombie_detection()
        log_list = []
        mask_exhaustion=[i for i in range(8)]

        # mask_exhaustion = zd.exhaustion()
        # log_list.append(zd.get_model(mask=mask_exhaustion, model_name='svc_e_{}.model'.format(i)))

        mask_filter = zd.feature_selection_filter(f_num=len(mask_exhaustion))
        log_list.append(zd.get_model(mask=mask_filter, model_name='svc_f_{}.model'.format(i)))

        mask_wrapper = zd.feature_selection_wrapper(f_num=len(mask_exhaustion))
        log_list.append(zd.get_model(mask=mask_wrapper, model_name='svc_w_{}.model'.format(i)))

        log_list.append(zd.get_model(model_name='svc_{}'.format(i)))

        with open('log_{}.txt'.format(i), 'w') as f:
            f.writelines(str(mask_exhaustion) + '\n')
            f.writelines(str(mask_filter) + '\n')
            f.writelines(str(mask_wrapper) + '\n')
            for i in log_list:
                f.writelines(str(i) + '\n')

def multi_test(mask):
    log_list = []
    for i in range(100):
        zd = zombie_detection()
        zd.get_model(mask=best_mask_2)
        log_list.append(zd.get_model(mask=best_mask_2,model_name='svc_1.model'))

    test_ave=0
    val_ave=0
    tran_ave=0
    P_ave=0
    R_ave=0
    F_ave=0
    for i in log_list:
        test_ave+=i['test']
        val_ave+=i['val']
        tran_ave+=i['train']
        P_ave+=i['P']
        R_ave+=i['R']
        F_ave+=i['F']
    my_len=len(log_list)
    print('test',test_ave/my_len)
    print('val',val_ave/my_len)
    print('train',tran_ave/my_len)
    print('P',P_ave/my_len)
    print('R',R_ave/my_len)
    print('F',F_ave/my_len)




if __name__ == '__main__':
    main()



