import requests
import re
import json

def main():
    pass

def crawl_weibo(id):
    result=requests.get(url='https://m.weibo.cn/status/{}'.format(id))
    search_str_list=['attitudes_count','comments_count','reposts_count']
    post_dict={}
    for search_str in search_str_list:
        searchobj = re.search(r'"{}": (.+),'.format(search_str), result.text)
        if searchobj:
            post_dict[search_str]=searchobj.group(1)
        else:
            return 0
    searchobj = re.search(r'"{}": "(.+)",'.format('text'), result.text)
    post_dict['text']=searchobj.group(1)
    searchobj=re.search(r'"{}": "(.+)",'.format('longTextContent'), result.text)
    if searchobj:
        post_dict['retweeted_status']=True
        post_dict['retweeted_text']=searchobj.group(1)
    else:
        post_dict['retweeted_status'] = False
    return post_dict

def check_user_exist(id):
    result=requests.get(url='https://m.weibo.cn/api/container/getIndex?containerid=230283{}_-_INFO'.format(id))
    cards = json.loads(result.text)['data']['cards']
    print(len(cards))
    for card in cards:
        if 'card_group' in card:
            for sub_card in card['card_group']:
                if 'item_name' in sub_card and sub_card['item_name'] == '所在地':
                    return True
    return False



def main():
    print(check_user_exist(327912873321201))

if __name__ == '__main__':
    main()