from rest_framework import serializers
from .models import Tweet
from django.conf import settings

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH
TWEET_ACTION_OPTION = settings.TWEET_ACTION_OPTION


class TweetActionSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()

    def validated_action(self, value):
        value = value.lower().strip()
        if value not in TWEET_ACTION_OPTION:
            raise serializers.ValidationError("NOT A VALID ACTION")
        return value


class TweetSerializers(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Tweet
        fields = ['id', 'content', 'likes']


    def get_likes(self,obj):
        return obj.likes.count()


    def validated_content(self, value):
        if len(value) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError("This Tweet Is Way Too Long")
        return value
