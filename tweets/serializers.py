from rest_framework import serializers
from .models import Tweet
from django.conf import settings

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH


class TweetSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ['content']

    def validated_content(self, value):
        if len(value) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError("This Tweet Is Way Too Long")
        return value
