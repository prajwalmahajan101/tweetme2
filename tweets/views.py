from django.shortcuts import render, redirect
import random

from django.http import JsonResponse
from django.utils.http import is_safe_url
from django.conf import settings

from .form import Tweetfrom
from .models import Tweet

# Create your views here.

ALLOWED_HOST = settings.ALLOWED_HOSTS


def home_view(request, *args, **kwargs):
    # return HttpResponse("<h1>Hello World</h1>")
    return render(request, "pages/home.html", context={}, status=200)


def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    tweet_list = [x.serialize() for x in qs]
    data = {
        'isUser': False,
        'response': tweet_list
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
    next_url = request.POST.get("next") or None

    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)
        if next_url != None and is_safe_url(next_url, ALLOWED_HOST):
            return redirect(next_url)
        form = Tweetfrom()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html', context={"form": form})
