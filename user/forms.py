from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Monetization, AdminUpload

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'User With This Email Already Exist')
        return email


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    YEARS= [x for x in range(1904,2020)]    
    content = forms.CharField(label="Bio",  required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Bio Goes Here', 'rows': '4', 'cols': '30'}))
    # gender = forms.ChoiceField(choices=GENDER_CHOICES,required=True)
    cv = forms.FileField(label="Upload Your CV If You Intend On Applying For A Job Through The Website: ", widget=forms.ClearableFileInput(attrs={'accept': ".pdf, .docx"}), required=False)
    birth_date= forms.DateField(label='What is your birth date?', initial="1990-06-21", widget=forms.SelectDateWidget(years=YEARS),required=True)
    class Meta:
        model = Profile
        fields = ('image', 'content', 'gender', 'birth_date', 'cv')


class MonetizeForm(forms.ModelForm):
    account_name = forms.CharField(label="Account Name", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Account Name', 'rows': '1', 'cols': '30'}))
    account_num = forms.CharField(label="Account Number", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Account Number', 'rows': '1', 'cols': '10'}))

    class Meta:
        model = Monetization
        fields = ['bank', 'account_name', 'account_num']

class AdminUp(forms.ModelForm):

    class Meta:
        model = AdminUpload
        exclude = ['user']