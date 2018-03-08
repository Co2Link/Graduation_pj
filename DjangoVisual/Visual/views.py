from django.shortcuts import render
from django.http import JsonResponse
from my_main.models import ScrapyItem
from django.views.decorators.csrf import csrf_exempt
from .matplot_visual import post_freq,fans_num,gender
from scrapyd_api import ScrapydAPI

# Create your views here.
scrapyd = ScrapydAPI('http://localhost:6800')
@csrf_exempt
def search_user(request):
    id = request.POST.get('id', None)  # take url comes from client. (From an input may be?)
    if not id:
        return render(request, 'Visual/dashboard.html', context={'tips': '请输入id', 'pics': False})

    if not id.isdigit():
        return render(request, 'Visual/dashboard.html', context={'tips': '请输入id', 'pics': False})

    result=ScrapyItem.objects.filter(id=id) #查询是否已经执行过该id的爬虫
    if result:
        status = scrapyd.job_status('default', result[0].task_id)
        if status=='running':  #未查询到任务，则返回空字符串
            return render(request,'Visual/dashboard.html',context={'tips':'爬取数据中，请等待','pics':False})
        else:
            post_freq(id)
            gender(id)
            fans_num(id)
            return render(request, 'Visual/dashboard.html', context={'tips': '用户id: {}'.format(id), 'pics': True})
    else:
        task = scrapyd.schedule('default', 'fans', id=id)
        item=ScrapyItem(id=id,task_id=task)
        item.save()
        return render(request,'Visual/dashboard.html',context={'tips':'开始爬取数据，请等待'})

def index(request):
    return render(request,'Visual/dashboard.html',context={'tips':'消息提示','pics':False})
