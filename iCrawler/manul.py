import requests


def main():
    # result=requests.post(url='http://127.0.0.1:8000/api/crawl/',data={'url':'http://bbs.ooro2.com/'})
    result = requests.get(url='http://127.0.0.1:8000/api/crawl/', params={"task_id": "b75a82d81e2311e89f78001a7dda7113", "unique_id": "ad064f9b-fef3-4270-839f-d3e9b6a35b38"})
    print(result.text)

if __name__=='__main__':
    main()


