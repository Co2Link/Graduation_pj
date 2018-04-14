from Visual.ass.matplot_visual import create_pic
import sys
import time

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