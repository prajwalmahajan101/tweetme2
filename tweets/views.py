from django.shortcuts import render, redirect
import random
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

from django.http import JsonResponse
from django.utils.http import is_safe_url
from django.conf import settings

from .form import Tweetfrom
from .models import Tweet
from .serializers import TweetSerializers, TweetActionSerializers

# Create your views here.

ALLOWED_HOST = settings.ALLOWED_HOSTS


def home_view(request, *args, **kwargs):
    # return HttpResponse("<h1>Hello World</h1>")
    return render(request, "pages/home.html", context={}, status=200)


@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    serializer = TweetSerializers(qs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = TweetSerializers(obj)
    return Response(serializer.data)


@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message": "You Can not delete this tweet"}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({"message": "You Removed Tweet "}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):
    serializer = TweetActionSerializers(request.POST)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")
        qs = Tweet.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == 'like':
            obj.likes.add(request.user)
        elif action == 'unlike':
            obj.likes.remove(request.user)
        elif action == 'retweet':
            pass

    return Response({"message": "You Removed Tweet "}, status=200)


@api_view(['POST'])
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetSerializers(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)


def tweet_create_view_pure_django(request, *args, **kwargs):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = Tweetfrom(request.POST or None)
    next_url = request.POST.get("next") or None

    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user
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


def tweet_list_view_pure_django(request, *args, **kwargs):
    qs = Tweet.objects.all()
    tweet_list = [x.serialize() for x in qs]
    data = {
        'isUser': False,
        'response': tweet_list
    }
    return JsonResponse(data)


def tweet_detail_view_pure_django(request, tweet_id, *args, **kwargs):
    data = {
        "id": tweet_id,
        # "image_path":obj.image.url
    }
    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = "No Data Found"
        status = 404
    return JsonResponse(data, status=status)
