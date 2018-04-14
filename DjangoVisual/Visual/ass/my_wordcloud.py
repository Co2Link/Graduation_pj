from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt
import jieba
import pymongo as pymongo
from html.parser import HTMLParser
from snownlp import SnowNLP,sentiment


from wordcloud import WordCloud,ImageColorGenerator

def add_word(list):
    for items in list:
        jieba.add_word(items)
# add_word(my_words_list)
# text = open(path.join(d, text_path),'rb').read()
def jiebaclearText(text,stopwords_path,my_word_list_del):
    mywordlist = []
    seg_list = jieba.cut(text, cut_all=False)
    liststr="/ ".join(seg_list)
    with open(stopwords_path,'r',encoding='utf-8') as f:
        f_stop_seg_list = f.readlines()
        f_stop_seg_list = [i.strip() for i in f_stop_seg_list]
    for myword in liststr.split('/'):
        if not(myword.strip() in f_stop_seg_list) and len(myword.strip())>1:
            mywordlist.append(myword)

    clean_word_list=[]
    for i in mywordlist:
        if not i.strip() in my_word_list_del:
            clean_word_list.append(i)
    return ''.join(clean_word_list)

def dealHtmlTags(html):
    '''''
    去掉html标签
    '''
    html=html.strip()
    html=html.strip("\n")
    result=[]
    parse=HTMLParser()
    parse.handle_data=result.append
    parse.feed(html)
    parse.close()
    return "".join(result)

def create_wordcloud(text):
    text=dealHtmlTags(text)

    max_words=int(len(text)/30)
    if max_words<3:
        max_words=3
    elif max_words>20:
        max_words=20

    my_word_list=['路明非']
    add_word(my_word_list)

    font_path = 'D:/Python/Graduation_pj/DjangoVisual/Visual/ass/wordcloud_file/simkai.ttf'  # 为matplotlib设置中文字体路径没
    stopwords_path = 'D:/Python/Graduation_pj/DjangoVisual/Visual/ass/wordcloud_file/stopwords1893.txt'  # 停用词词表

    # 设置词云属性
    wc = WordCloud(font_path=font_path,  # 设置字体
                   background_color="white",  # 背景颜色
                   max_words=max_words,  # 词云显示的最大词数
                   max_font_size=100,  # 字体最大值
                   random_state=10,
                   width=800, height=600, margin=2,collocations=False  # 设置图片默认的大小,但是如果使用背景图片的话,那么保存的图片大小将会按照其大小保存,margin为词语边缘距离
                   )
    ## 需要去掉的词
    my_word_list_del=['网页','微博','链接','全文','回复','啊啊','啊啊啊','哈哈','哈哈哈','哈哈哈哈','啊啊啊啊']
    text = jiebaclearText(text,stopwords_path,my_word_list_del)
    wc.generate(text)

    plt.figure()
    # 以下代码显示图片
    plt.imshow(wc)
    plt.axis("off")
    # plt.show()

    wc.to_file('D:/Python/Graduation_pj/DjangoVisual/static/images/single_weibo.png')
    plt.close()

def main():
    CONN=pymongo.MongoClient('localhost',27017)
    col=CONN['syn_12']['comments']

    post_id=4226462758878143

    text_list=list(col.find({'post_id':post_id}))
    text=''
    for i in text_list:
        text+=' '+i['text']
    create_wordcloud(text)


if __name__ == '__main__':
    main()

