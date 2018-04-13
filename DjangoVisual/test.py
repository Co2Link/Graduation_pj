import datetime
import requests
import re
from snownlp import SnowNLP

def main():
    my_str='草你妈'
    s=SnowNLP(my_str)
    score=s.sentiments
    print('sentiment: {}'.format(score))






if __name__ == '__main__':
    main()