from django import forms

from .models import Post, Location
from .prefectures import PREFECTURE_CHOICES


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['body'].label = '投稿内容' # labelの文字を変更

    body = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'input mb-5'
        }
    ))

    class Meta:
        model = Post 
        exclude = ['author', 'location']
    
    prefix = 'post'


class LocationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'スケートパーク名'
        self.fields['prefecture'].label = '都道府県'
        self.fields['city'].label = '市町村'
        self.fields['location_image'].label = '写真'

    name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'input mb-5'
        }
    ))

    prefecture = forms.ChoiceField(
        choices = PREFECTURE_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'select mb-5'
            }
        ) 
    )

    city = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'input mb-5',
        }
    ))

    location_image = forms.ImageField(widget=forms.FileInput(
        attrs={
            'class': 'mb-5'
        }
    ))

    class Meta:
        model = Location
        fields = ['name', 'prefecture', 'city', 'location_image']

    prefix = 'location'