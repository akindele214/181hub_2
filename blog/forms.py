from .models import Comment, Post, Share, Images, Quote, Report , WebGroup, GroupPost
from django.contrib.auth.models import User
from django import forms


# 'photo_path': forms.ClearableFileInput(attrs={'multiple': True}),
class GroupCreateForm(forms.ModelForm):
    group_name = forms.Textarea()

    class Meta:
        model = WebGroup
        fields = ('group_name',)


class GroupPostCreateForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Talk Your Own', 'rows': '4', 'cols': '30'}))
    
    class Meta:
        model = GroupPost
        fields = ('content',)


class PostCreateForm(forms.ModelForm):
    video = forms.FileField(label="Upload Video(.mp4) File Less Than 50MB", widget=forms.ClearableFileInput(attrs={'accept': ".mp4"}), required=False)
    audio = forms.FileField(label="Upload Audio File(.mp3) File Less Than 11MB", widget=forms.ClearableFileInput(attrs={'accept': ".mp3"}), required=False)

    class Meta:
        model = Post
        fields = (
            'title',
            'content',
            'restrict_comment',
            'video',
            'audio',
        )


class PostEditForm(forms.ModelForm):
    video = forms.FileField(label="Upload Video(.mp4) File Less Than 50MB", widget=forms.ClearableFileInput(attrs={'accept': ".mp4"}), required=False)
    audio = forms.FileField(label="Upload Audio File(.mp3) File Less Than 11MB", widget=forms.ClearableFileInput(attrs={'accept': ".mp3"}), required=False)

    class Meta:
        model = Post
        fields = (
            'title',
            'content',
            'restrict_comment',
            'video',
            'audio',
        )


class CommentForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Comment Goes Here', 'rows': '4', 'cols': '30'}))

    class Meta:
        model = Comment
        fields = ('content',)


class SearchForm(forms.ModelForm):
    search = forms.CharField()

    class Meta:
        model = User
        fields = ('search',)



class ShareForm(forms.ModelForm):
    content = forms.CharField(label="", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Talk Your Own', 'rows': '4', 'cols': '30'}))

    class Meta:
        model = Share
        fields = ['content', 'image']

    def __init__(self, *args, **kwargs):
        super(ShareForm, self).__init__(*args, **kwargs)
        self.fields['content'].required = False


class QuoteForm(forms.ModelForm):
    content = forms.CharField(label="", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Talk Your Own', 'rows': '4', 'cols': '30'}))

    class Meta:
        model = Share 
        fields = ['content', 'image']
    
    # def __init__(self, *args, **kwargs):
    #     super(QuoteForm, self).__init__(*args, **kwargs)
    #     self.fields['content'].required = False


class ShareEditForm(forms.ModelForm):
    class Meta:
        model = Share
        fields = ['content', 'image']


class ReportForm(forms.ModelForm):
    content = forms.CharField(label="", required=True, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Report Goes Here', 'rows': '4', 'cols': '30'}))
    
    class Meta:
        model= Report
        fields = ['content']
