from django.shortcuts import render
from my_main.models import ScrapyItem,UserItem_dj,post_Item_dj,new_post_Item_dj,comments_Item_dj
from django.views.decorators.csrf import csrf_exempt
from Visual.ass.matplot_visual import create_pic,sentiment_pic,sentiment_pic_multi
from scrapyd_api import ScrapydAPI
from Visual.ass.data import location_count
import json,time
from Visual.ass.crawl import crawl_weibo,check_user_exist
from django.views.generic import ListView
from Visual.ass.my_wordcloud import create_wordcloud,dealHtmlTags
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Create your views here.
scrapyd = ScrapydAPI('http://localhost:6800')
@csrf_exempt
def search_user(request):
    id = request.POST.get('id', None)  # take url comes from client. (From an input may be?)
    ## 检测id合理性
    if not id:
        return render(request, 'Visual/dashboard.html', context={'tips': '请输入id', 'pics': False})

    if not id.isdigit():
        return render(request, 'Visual/dashboard.html', context={'tips': '请输入id', 'pics': False})

    ## 检测该用户是否存在
    if check_user_exist(id):
        result=ScrapyItem.objects.filter(id=id) #查询是否已经执行过该id的爬虫
        if result:
            status = scrapyd.job_status('default', result[0].task_id)
            if status=='running':  #未查询到任务，则返回空字符串
                return render(request,'Visual/dashboard.html',context={'tips':'爬取数据中，请等待','pics':False})
            else:
                creation=create_pic(id)
                creation.gender()
                creation.fans_num()
                creation.post_freq()
                creation.get_pic()
                creation.fans_authen()

                text = ''
                for i in post_Item_dj.objects.filter(author_id=id):
                    text += i.text
                create_wordcloud(text)

                user=UserItem_dj.objects.get(id=id)
                if user.gender=='m':
                    dgender='男'
                else:
                    dgender='女'
                if user.verified_type == -1:
                    verified_type = '普通'
                elif user.verified_type == 200:
                    verified_type = '初级达人'
                elif user.verified_type == 220:
                    verified_type = '高级达人'
                elif user.verified_type == 0:
                    verified_type = '黄V'
                else:
                    verified_type='蓝V'
                user_info_dict={'user_name':user.screen_name, 'description':user.description,
                                'location':user.location,'follow_count':user.follow_count,
                                'followers_count':user.followers_count,'gender':dgender,
                                'statuses_count':user.statuses_count,'verified_type':verified_type}
                return render(request, 'Visual/dashboard.html', context={'tips': '用户id: {}'.format(id), 'pics': True,'user_info_dict':user_info_dict,'option_js':json.dumps(location_count(id))})
        else:
            task = scrapyd.schedule('default', 'fans', id=id)
            item=ScrapyItem(id=id,task_id=task)
            item.save()
            return render(request,'Visual/dashboard.html',context={'tips':'开始爬取数据，请等待'})
    else:
        return render(request, 'Visual/dashboard.html', context={'tips': '该id不存在'})


def index(request):
    return render(request,'Visual/dashboard.html',context={'tips':'请输入用户id','pics':False})

class UserView(ListView):
    model = UserItem_dj
    template_name = 'Visual/listing.html'
    context_object_name = 'user_list'
    paginate_by = 5

class weiboView(ListView):
    model = new_post_Item_dj
    template_name = 'Visual/listing_weibo.html'
    context_object_name = 'post_list'
    paginate_by = 5

def comments(request,post_id):
    comments_list = comments_Item_dj.objects.filter(post_id=post_id)

    paginator = Paginator(comments_list, 5) # 每页显示 25 个联系人

    page = request.GET.get('page')
    # print('page :{}'.format(page))
    if page==None:   ##只在跳转到第一页时更新图片，节省后面翻页时的刷新时间
        text = ''
        text_list = []
        for i in comments_list:
            text += i.text
            text_list.append(i.text)
        create_wordcloud(text)
        sentiment_pic(text_list)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果用户请求的页码号不是整数，显示第一页
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果用户请求的页码号超过了最大页码号，显示最后一页
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'Visual/comments.html', {'contacts': contacts,'tips':'微博id: {}'.format(post_id),'post_id':post_id})


def show(request,id):
    ## 防止在用户一览表中点击正在爬取数据的用户
    result = ScrapyItem.objects.filter(id=id)
    status = scrapyd.job_status('default', result[0].task_id)
    if status == 'running':
        return render(request, 'Visual/dashboard.html', context={'tips': '爬取数据中，请等待', 'pics': False})
    ##pic
    start=time.time()
    creation = create_pic(id)
    creation.gender()
    creation.fans_num()
    creation.post_freq()
    creation.get_pic()
    creation.fans_authen()
    end=time.time()
    print('pic time: {}'.format(str(end-start)))
    text=''
    for i in post_Item_dj.objects.filter(author_id=id):
        text+=i.text
    create_wordcloud(text)
    ##data
    user = UserItem_dj.objects.get(id=id)
    if user.gender == 'm':
        dgender = '男'
    else:
        dgender = '女'
    if user.verified_type == -1:
        verified_type = '普通'
    elif user.verified_type == 200:
        verified_type = '初级达人'
    elif user.verified_type == 220:
        verified_type = '高级达人'
    elif user.verified_type == 0:
        verified_type = '黄V'
    else:
        verified_type = '蓝V'
    user_info_dict = {'user_name': user.screen_name, 'description': user.description,
                      'location': user.location, 'follow_count': user.follow_count,
                      'followers_count': user.followers_count, 'gender': dgender,
                      'statuses_count': user.statuses_count, 'verified_type': verified_type}
    return render(request, 'Visual/dashboard.html',
                  context={'tips': '用户id: {}'.format(id), 'pics': True, 'user_info_dict': user_info_dict,
                           'option_js': json.dumps(location_count(id))})
@csrf_exempt
def search_weibo(request):
    id = request.POST.get('id', None)
    if not id:  #检测输入合法性
        return render(request, 'Visual/weibo.html', context={'tips': '请输入微博id'})
    if not id.isdigit():
        return render(request, 'Visual/weibo.html', context={'tips': '请输入微博id，数字'})

    result=ScrapyItem.objects.filter(id=str(id))
    if result :  #查找是否已经爬取
        status = scrapyd.job_status('default', result[0].task_id)
        if status=='running':   #检测是否正在爬
            return render(request, 'Visual/weibo.html', context={'tips': '正在爬取数据，请等待'})
        else:
            post=new_post_Item_dj.objects.get(id=id)
            comments_list = comments_Item_dj.objects.filter(post_id=id)
            create_wordcloud(post.text)
            sentiment_pic(dealHtmlTags(post.text))
            return render(request,'Visual/weibo.html',context={'tips':'微博id: {}'.format(id),'post':post,'comments_list':comments_list})
    else:
        post_dict = crawl_weibo(id)
        if post_dict!=0: #检测微博是否存在
            post=new_post_Item_dj(**post_dict)
            post.save()
            task_id = scrapyd.schedule('default', 'comments', id=id) #启动爬虫
            item=ScrapyItem(id=id,task_id=task_id)
            item.save()                         #存储ScrapyItem 用于查询爬虫状态
            return render(request, 'Visual/weibo.html', context={'tips': '开始爬取数据，请等待'})
        else:
            return render(request, 'Visual/weibo.html', context={'tips': '微博id不存在'})

def weibo(request):
    return render(request, 'Visual/weibo.html',context={'tips':'请输入微博id'})

def show_weibo(request,id):
    if not id:  # 检测输入合法性
        return render(request, 'Visual/weibo.html', context={'tips': '请输入微博id'})
    if not id.isdigit():
        return render(request, 'Visual/weibo.html', context={'tips': '请输入微博id，数字'})
    result = ScrapyItem.objects.filter(id=str(id))
    if result:  # 查找是否已经爬取
        status = scrapyd.job_status('default', result[0].task_id)
        if status == 'running':  # 检测是否正在爬
            return render(request, 'Visual/weibo.html', context={'tips': '正在爬取数据，请等待'})
        else:
            post = new_post_Item_dj.objects.get(id=id)
            comments_list = comments_Item_dj.objects.filter(post_id=id)
            create_wordcloud(post.text)
            sentiment_pic(dealHtmlTags(post.text))
            return render(request, 'Visual/weibo.html',
                          context={'tips': '微博id: {}'.format(id), 'post': post, 'comments_list': comments_list})
    else:
        post_dict = crawl_weibo(id)
        if post_dict != 0:  # 检测微博是否存在
            post = new_post_Item_dj(**post_dict)
            post.save()
            task_id = scrapyd.schedule('default', 'comments', id=id)  # 启动爬虫
            item = ScrapyItem(id=id, task_id=task_id)
            item.save()  # 存储ScrapyItem 用于查询爬虫状态
            return render(request, 'Visual/weibo.html', context={'tips': '开始爬取数据，请等待'})
        else:
            return render(request, 'Visual/weibo.html', context={'tips': '微博id不存在'})