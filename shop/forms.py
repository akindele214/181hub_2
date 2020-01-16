from .models import Product
from django.contrib.auth.models import User
from django import forms


CATEGORY_CHOICES = [
    ('', 'Select Category'),
    ('Accommodation', 'Accommodation'),
    ('Sound Devices', 'Sound Devices'),
    ('Cell/Mobile/Wireless Phones', 'Cell/Mobile/Wireless Phones'),
    ('Books', 'Books'),
    ('Computers', 'Computers'),
    ('TVs', 'TVs'),
    ('Cosmetics', 'Cosmetics'),
    ('Miscellaneous', 'Miscellaneous')
]

class ProductCreateForm(forms.ModelForm):
    prod_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item Name', 'rows': '4', 'cols': '30'}))
    prod_details = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Item Description', 'rows': '4', 'cols': '30'}))
    prod_price = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item Price'}))
    prod_location = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item Location'}))
    phone_number = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}), required=False)
    prod_category = forms.ChoiceField(label='Item Category', initial='', widget=forms.Select(), choices=CATEGORY_CHOICES ,required=True)
    #prod_category = forms.MultipleChoiceField(label='Item Category',widget=forms.Mu(), choices=CATEGORY_CHOICES ,required=True)
    #content = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Talk Your Own', 'rows': '4', 'cols': '30'}))

    class Meta:
        model = Product
        fields = (
            'prod_name', 
            'prod_details', 
            'prod_price', 
            'prod_location', 
            'phone_number',
            'prod_category',
            )