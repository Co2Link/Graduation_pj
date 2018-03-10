import requests
import re

def main():
    pass

def crawl_weibo(id):
    result=requests.get(url='https://m.weibo.cn/status/{}'.format(id))
    search_str_list=['attitudes_count','comments_count','reposts_count']
    post_dict={}
    for search_str in search_str_list:
        searchobj = re.search(r'"{}": (.+),'.format(search_str), result.text)
        post_dict[search_str]=searchobj.group(1)
    searchobj = re.search(r'"{}": "(.+)",'.format('text'), result.text)
    post_dict['text']=searchobj.group(1)
    return post_dict

if __name__ == '__main__':
    main()