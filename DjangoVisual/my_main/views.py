from django.shortcuts import render

from uuid import uuid4
from urllib.parse import urlparse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from scrapyd_api import ScrapydAPI
from .models import UserItem_dj,fans_1_Item_dj,fans_2_Item_dj,post_Item_dj

scrapyd = ScrapydAPI('http://localhost:6800')

@csrf_exempt
@require_http_methods(['POST', 'GET'])  # only get and post
def crawl(request):
    # Post requests are for new crawling tasks
    if request.method == 'POST':
        id = request.POST.get('id', None)  # take url comes from client. (From an input may be?)
        if not id:
            return JsonResponse({'error': 'Missing  args'})
        if not id.isdigit():
            return JsonResponse({'error': 'id is invalid'})
        task = scrapyd.schedule('default', 'fans',id=id)
        return JsonResponse({'task_id': task, 'id': id, 'status': 'started'})

    elif request.method == 'GET':
        task_id = request.GET.get('task_id', None)
        if not task_id:
            return JsonResponse({'error': 'Missing args'})
        status = scrapyd.job_status('default', task_id)
        return JsonResponse({'status': status})

def clean(request):
    item_list=UserItem_dj.objects.all()
    for i in item_list:
        i.delete()
    item_list=post_Item_dj.objects.all()
    for i in item_list:
        i.delete()
    item_list=fans_1_Item_dj.objects.all()
    for i in item_list:
        i.delete()
    item_list=fans_2_Item_dj.objects.all()
    for i in item_list:
        i.delete()
    return JsonResponse({'status':'clean_started'})