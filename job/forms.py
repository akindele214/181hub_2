from .models import JobOpening, ShareJob
from django.contrib.auth.models import User
from django import forms



EDUCATION_CHOICES = [
    ('First School Leaving Certificate (FSLC)', 'First School Leaving Certificate (FSLC)'),
    ('Secondary School (SSCE)', 'Secondary School (SSCE)'),
    ('NCE', 'NCE'),
    ('OND', 'OND'),
    ('BA/BSc/HND', 'BA/BSc/HND'),
    ('MBA/MSc/MA', 'MBA/MSc/MA'),
    ('PhD/Fellowship', 'PhD/Fellowship'),
    ('Vocational', 'Vocational'),
    ('Others', 'Others'),
]
STATE_CHOICES =  [       
            ('Abia', 'Abia'),
            ('Abuja','Abuja'),
            ('Adamawa', 'Adamawa'),
            ('Akwa Ibom', 'Akwa Ibom'),
            ('Anambra', 'Anambra'),
            ('Bauchi', 'Bauchi'),
            ('Bayelsa', 'Bayelsa'),
            ('Benue', 'Benue',),
            ('Borno', 'Borno'),
            ('Cross River', 'Cross River'),
            ('Delta', ' Delta'),
            ('Ebonyi', 'Ebonyi'),
            ('Edo', 'Edo'),
            ('Ekiti', 'Ekiti'),
            ('Enugu', 'Enugu'),
            ('Gombe', 'Gombe'),
            ('Imo', 'Imo'),
            ('Jigawa', 'Jigawa'),
            ('Kaduna', 'Kaduna'),
            ('Kano', 'Kano'),
            ('Katsina', 'Katsina'),
            ('Kebbi', 'Kebbi'),
            ('Kogi', 'Kogi'),
            ('Kwara', 'Kwara'),
            ('Lagos', 'Lagos'),
            ('Nasarawa', 'Nasawara'),
            ('Niger', 'Niger'),
            ('Ogun', 'Ogun'),
            ('Ondo', 'Ondo'),
            ('Osun', 'Osun'),
            ('Other', 'Other'),
            ('Oyo', 'Oyo'),
            ('Plateau', 'Plateau'),
            ('Rivers', 'Rivers'),
            ('Sokoto', 'Sokoto'),
            ('Taraba', 'Taraba'),
            ('Yobe', 'Yobe'),
            ('Zamfara', 'Zamfara'),
    ]

class CreateJobForm(forms.ModelForm):
    # state = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=STATE_CHOICES)
    # education = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=EDUCATION_CHOICES)
    job_description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': '', 'rows': '8', 'cols': '30'}))
    method_of_application = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': '', 'rows': '8', 'cols': '30'}))
    # send_cv_directly = forms.BooleanField(label="Click if You'd Like Applicants to Send CV Directly",required=False)
    company_email = forms.EmailField(widget=forms.TextInput(attrs={'type': 'email','placeholder': "Enter An Email An Applicant Can Send An Application To."}))

    class Meta:
        model = JobOpening
        fields = (
            'job_title',
            'company_description',
            'job_description',
            'company_name',
            'job_type',
            'education',
            'industry',
            'field',
            'state',
            'company_email',
            'experience',
            'method_of_application',
            # 'send_cv_directly',
        )


class CreateShareForm(forms.ModelForm):
    content = forms.CharField(label="", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Share...', 'rows': '4', 'cols': '30'}))
    class Meta:
        model = ShareJob
        fields = [
            'content',
            'image',
        ]
    def __init__(self, *args, **kwargs):
        super(CreateShareForm, self).__init__(*args, **kwargs)
        self.fields['content'].required = False

class ShareJobEditForm(forms.ModelForm):
    class Meta:
        model = ShareJob
        fields = ['content', 'image']
    def __init__(self, *args, **kwargs):
        super(ShareJobEditForm, self).__init__(*args, **kwargs)
        self.fields['content'].required = False        

class QuoteJobForm(forms.ModelForm):
    content = forms.CharField(label="", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Talk Your Own', 'rows': '4', 'cols': '30'}))

    class Meta:
        model = ShareJob 
        fields = ['content', 'image']
    
    def __init__(self, *args, **kwargs):
        super(QuoteJobForm, self).__init__(*args, **kwargs)
        self.fields['content'].required = False    