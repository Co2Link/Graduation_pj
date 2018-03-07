import  requests

def clean():
    result=requests.get(url='http://127.0.0.1:8000/api/clean/')
    print(result.text)
def crawl(id):
    result=requests.post(url='http://127.0.0.1:8000/api/crawl/', data={"id":id})
    print(result.text)



def main():
    # clean()
    nine=3279873201
    a=1880564361
    b=3912883937
    c=5723240588
    crawl(b)





if __name__=='__main__':
    main()