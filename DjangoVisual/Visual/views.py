from django.shortcuts import render
from django.http import JsonResponse
from my_main.models import UserItem_dj,fans_2_Item_dj,fans_1_Item_dj,post_Item_dj
# Create your views here.

def search_user(request,id):
    result=UserItem_dj.objects.filter(id=id)
    if result.exists():
        return JsonResponse(data={'result':'exist'})
    else:
        return JsonResponse(data={'result':'not exist'})


def dashboard(request):
    return render(request,'Visual/dashboard.html')

def dashboard(request):
    return render(request,'Visual/dashboard.html')

def dashboard(request):
    return render(request,'Visual/dashboard.html')

def dashboard(request):
    return render(request,'Visual/dashboard.html')