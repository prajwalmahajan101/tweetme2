import random
from django.shortcuts import render
from django.http import JsonResponse

from .form import Tweetfrom
from .models import Tweet

# Create your views here.

def home_view(request,*args, **kwargs):
    # return HttpResponse("<h1>Hello World</h1>")
    return render(request,"pages/home.html",context={},status=200)

def tweet_list_view(request,*args,**kwargs):
    qs = Tweet.objects.all()
    tweet_list = [{'id':x.id,'content':x.content,'likes': random.randint(0,1234)} for x in qs]
    data={
        'isUser' : False,
        'response' : tweet_list
    }
    return JsonResponse(data)

def tweet_detail_view(request,tweet_id,*args, **kwargs):
    data={
        "id":tweet_id,
        #"image_path":obj.image.url
    }
    status=200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content']= obj.content
    except:
        data['message']= "No Data Found"
        status = 404
    return JsonResponse(data,status=status)

def tweet_create_view(request, *args, **kwargs):
    form = Tweetfrom(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        form = Tweetfrom()
    return render(request, 'components/form.html', context={"form": form})
