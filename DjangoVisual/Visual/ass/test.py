from Visual.ass.matplot_visual import create_pic
import sys
import time

def my_test(url):
    import requests
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1;'
                      ' en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }
    result = requests.get(url=url,headers=headers)
    print(result.text)

def main():
    start=time.time()
    creation = create_pic(2842266491)
    creation.gender()
    creation.fans_num()
    creation.post_freq()
    creation.get_pic()
    creation.fans_authen()
    end=time.time()
    print('time: {}'.format(end-start))
    # print(sys.path)

if __name__ == '__main__':
    main()