from django.contrib.auth.models import User
from django import forms
from .models import Chat

class ReportForm(forms.ModelForm):
    content = forms.CharField(label="", required=True, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Report Goes Here', 'rows': '4', 'cols': '30'}))
    
    class Meta:
        model= Chat
        fields = ['content']