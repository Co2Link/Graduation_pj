import  requests
def main():
    result=requests.post(url='http://127.0.0.1:8000/api/crawl/', data={"id":3597829674})
    # requests.get(url='http://127.0.0.1:8000/api/crawl/', params={"uniqe_id": uniqe_id, "task_id": task_id})
    print(result.text)




if __name__=='__main__':
    main()