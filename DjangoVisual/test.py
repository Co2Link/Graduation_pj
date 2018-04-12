import datetime
import requests
import re

def main():
    result = requests.get(url='https://m.weibo.cn/status/{}'.format(4227198048631523))
    print(result.text)
    result=re.findall(r'"reposts_count": (.+),',result.text)
    print(result[0])




if __name__ == '__main__':
    main()