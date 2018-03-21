import datetime
import pymongo as pymongo
### 生成EChart的option数据

# import random
# random.seed(datetime.datetime.now().second)
# option = {
#     'title' : {
#         'text': '粉丝地区分布',
#         'x':'center'
#     },
#     'tooltip' : {
#         'trigger': 'item'
#     },
#     'dataRange': {
#         'min': 0,
#         'max': 2500,
#         'x': 'right',
#         'y': 'bottom',
#         'text':['高','低'],           ##文本，默认为数值文本
#         'calculable' : 'true'
#     },
#     'series' : [
#         {
#             'name': '粉丝数',
#             'type': 'map',
#             'mapType': 'china',
#             'roam': False,
#             'itemStyle':{
#                 'normal':{'label':{'show':True}},
#                 'emphasis':{'label':{'show':True}}
#             },
#             'data':[
#                 {'name': '北京','value':random.randint(1,1000)},
#                 {'name': '天津','value':random.randint(1,1000)},
#                 {'name': '上海','value':random.randint(1,1000)},
#                 {'name': '重庆','value':random.randint(1,1000)},
#                 {'name': '河北','value':random.randint(1,1000)},
#                 {'name': '河南','value':random.randint(1,1000)},
#                 {'name': '云南','value':random.randint(1,1000)},
#                 {'name': '辽宁','value':random.randint(1,1000)},
#                 {'name': '黑龙江','value':random.randint(1,1000)},
#                 {'name': '湖南','value':random.randint(1,1000)},
#                 {'name': '安徽','value':random.randint(1,1000)},
#                 {'name': '山东','value':random.randint(1,1000)},
#                 {'name': '新疆','value':random.randint(1,1000)},
#                 {'name': '江苏','value':random.randint(1,1000)},
#                 {'name': '浙江','value':random.randint(1,1000)},
#                 {'name': '江西','value':random.randint(1,1000)},
#                 {'name': '湖北','value':random.randint(1,1000)},
#                 {'name': '广西','value':random.randint(1,1000)},
#                 {'name': '甘肃','value':random.randint(1,1000)},
#                 {'name': '山西','value':random.randint(1,1000)},
#                 {'name': '内蒙古','value':random.randint(1,1000)},
#                 {'name': '陕西','value':random.randint(1,1000)},
#                 {'name': '吉林','value':random.randint(1,1000)},
#                 {'name': '福建','value':random.randint(1,1000)},
#                 {'name': '贵州','value':random.randint(1,1000)},
#                 {'name': '广东','value':random.randint(1,1000)},
#                 {'name': '青海','value':random.randint(1,1000)},
#                 {'name': '西藏','value':random.randint(1,1000)},
#                 {'name': '四川','value':random.randint(1,1000)},
#                 {'name': '宁夏','value':random.randint(1,1000)},
#                 {'name': '海南','value':random.randint(1,1000)},
#                 {'name': '台湾','value':random.randint(1,1000)},
#                 {'name': '香港','value':random.randint(1,1000)},
#                 {'name': '澳门','value':random.randint(1,1000)}
#             ]
#         }
#     ]
# };

def location_count(id):         #生成location数据 dict
    id=str(id)
    CONN=pymongo.MongoClient('localhost',27017)
    cursor=CONN['syn_11']['fans_1'].find(filter={'master_id':id})
    # print(cursor.count())
    city_dict={}
    city_list=['北京', '天津', '上海', '重庆', '河北', '河南', '云南', '辽宁', '黑龙江', '湖南', '安徽', '山东', '新疆', '江苏', '浙江', '江西', '湖北', '广西', '甘肃', '山西', '内蒙古', '陕西', '吉林', '福建', '贵州', '广东', '青海', '西藏', '四川', '宁夏', '海南', '台湾', '香港', '澳门']
    for i in city_list:
        city_dict[i]=0
    for i in cursor:
        for city in city_list:
            if city in i['location']:
                city_dict[city]+=1
                break
    # print(city_dict)
    fix_data=[]
    max_num=0
    for key,value in city_dict.items():
        if max_num<value:
            max_num=value
        fix_data.append({'name':key,'value':value})
    option = {
        'title': {
            'text': '粉丝地区分布',
            'x': 'center'
        },
        'tooltip': {
            'trigger': 'item'
        },
        'dataRange': {
            'min': 0,
            'max': int(max_num),
            'x': 'right',
            'y': 'bottom',
            'text': ['高', '低'],  ##文本，默认为数值文本
            'calculable': 'true'
        },
        'series': [
            {
                'name': '粉丝数',
                'type': 'map',
                'mapType': 'china',
                'roam': False,
                'itemStyle': {
                    'normal': {'label': {'show': True}},
                    'emphasis': {'label': {'show': True}}
                },
                'data': fix_data
            }
        ]
    };
    return option

def main():
    nine=3279873201
    a=1880564361
    b=3912883937
    c=5723240588
    location_count("2745813247")




if __name__=='__main__':
    main()