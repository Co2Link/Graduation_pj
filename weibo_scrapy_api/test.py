import requests

def crawl_user(id):
    headers = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
               'Accept - Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
               'Connection': 'Keep-Alive',
               'Host': 'zhannei.baidu.com',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}
    result=requests.get(url='https://m.weibo.cn/api/container/getIndex?containerid=100505{}'.format(id))
    text=result.text
    print(type(text))
    print(text)

def proxy(id):
    # 代理服务器
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"

    # 代理隧道验证信息
    proxyUser = "H4NP63YB53Z83A3D"
    proxyPass = "38B0B9E121802BB5"

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
      "host" : proxyHost,
      "port" : proxyPort,
      "user" : proxyUser,
      "pass" : proxyPass,
    }

    proxies = {
        "http"  : proxyMeta,
        "https" : proxyMeta,
    }
    result = requests.get(url='https://m.weibo.cn/api/container/getIndex?containerid=100505{}'.format(id), proxies=proxies)
    print(result.status_code)
    print(result.text)

def main():
    id=3279873201
    crawl_user(id)
    print('分隔符--------')
    proxy(id)

if __name__ == '__main__':
    main()