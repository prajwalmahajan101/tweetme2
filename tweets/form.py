from django import forms
from .models import Tweet

MAX_TWEET_LENGTH = 240


class Tweetfrom(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) > MAX_TWEET_LENGTH:
            raise forms.ValidationError("This Tweet Is Way Too Long")
        return content
