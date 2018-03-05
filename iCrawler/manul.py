import requests


def main():
    result=requests.post(url='http://127.0.0.1:8000/api/crawl/',data={'url':'http://bbs.ooro2.com/'})
    print(result.text)


if __name__=='__main__':
    main()


