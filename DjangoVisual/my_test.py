import  requests
import sys
import os
def main():
    # id=123
    result=requests.post(url='http://127.0.0.1:8000/api/crawl/', data={"id":3597829674})
    # requests.get(url='http://127.0.0.1:8000/api/crawl/', params={"uniqe_id": uniqe_id, "task_id": task_id})
    print(result.text)

    # print(sys.path)
    # os.chdir('项目路径')
    # # 打印出项目路径下的目录
    # for file in os.listdir(os.getcwd()):
    #     print(file)


if __name__=='__main__':
    main()