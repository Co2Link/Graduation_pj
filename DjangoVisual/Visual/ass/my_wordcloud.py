from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt
import jieba
from html.parser import HTMLParser


from wordcloud import WordCloud,ImageColorGenerator

# 获取当前文件路径
# __file__ 为当前文件, 在ide中运行此行会报错,可改为
# d = path.dirname('.')
# d = path.dirname(__file__)
#
# stopwords = {}
# isCN = 1 #默认启用中文分词
# back_coloring_path = "wordcloud_file/timg.jpg" # 设置背景图片路径
# text_path = 'wordcloud_file/lz.txt' #设置要分析的文本路径
# font_path = 'wordcloud_file/simkai.ttf' # 为matplotlib设置中文字体路径没
# stopwords_path = 'wordcloud_file/stopwords1893.txt' # 停用词词表
# imgname1 = "WordCloudDefautColors.png" # 保存的图片名字1(只按照背景图片形状)
# imgname2 = "WordCloudColorsByImg.png"# 保存的图片名字2(颜色按照背景图片颜色布局生成)
#
# my_words_list = ['路明非'] # 在结巴的词库中添加新词
#
# back_coloring = imread(path.join(d, back_coloring_path))# 设置背景图片
#
# # 设置词云属性
# wc = WordCloud(font_path=font_path,  # 设置字体
#                background_color="white",  # 背景颜色
#                max_words=2500,  # 词云显示的最大词数
#                # mask=back_coloring,  # 设置背景图片
#                max_font_size=100,  # 字体最大值
#                random_state=10,
#                width=800, height=600, margin=2,# 设置图片默认的大小,但是如果使用背景图片的话,那么保存的图片大小将会按照其大小保存,margin为词语边缘距离
#                )
# 添加自己的词库分词
def add_word(list):
    for items in list:
        jieba.add_word(items)
# add_word(my_words_list)
# text = open(path.join(d, text_path),'rb').read()
def jiebaclearText(text,stopwords_path):
    mywordlist = []
    seg_list = jieba.cut(text, cut_all=False)
    liststr="/ ".join(seg_list)
    f_stop = open(stopwords_path,'rb')
    try:
        f_stop_text = f_stop.read( )
        f_stop_text=str(f_stop_text,'utf-8')
    finally:
        f_stop.close( )
    f_stop_seg_list=f_stop_text.split('\n')
    for myword in liststr.split('/'):
        if not(myword.strip() in f_stop_seg_list) and len(myword.strip())>1:
            mywordlist.append(myword)
    return ''.join(mywordlist)

# if isCN:
#     text = jiebaclearText(text,stopwords_path)
#
# # 生成词云, 可以用generate输入全部文本(wordcloud对中文分词支持不好,建议启用中文分词),也可以我们计算好词频后使用generate_from_frequencies函数
# wc.generate(text)
#
# plt.figure()
# # 以下代码显示图片
# plt.imshow(wc)
# plt.axis("off")
# plt.show()
# # 绘制词云
#
# # 保存图片
# wc.to_file(path.join(d, imgname1))

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
                   width=800, height=600, margin=2,  # 设置图片默认的大小,但是如果使用背景图片的话,那么保存的图片大小将会按照其大小保存,margin为词语边缘距离
                   )
    text = jiebaclearText(text,stopwords_path)

    wc.generate(text)

    plt.figure()
    # 以下代码显示图片
    plt.imshow(wc)
    plt.axis("off")
    # plt.show()

    wc.to_file('D:/Python/Graduation_pj/DjangoVisual/static/images/single_weibo.png')

def main():
    text = open('wordcloud_file/lz.txt', 'rb').read()
    create_wordcloud(text)

if __name__ == '__main__':
    main()

