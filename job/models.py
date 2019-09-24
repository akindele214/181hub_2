from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils import timezone 
from profanity.validators import validate_is_profane
from django.shortcuts import redirect, reverse
# Create your models here.


class JobManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(job_title__icontains=query)|
                         Q(job_description__icontains=query)|
                         Q(job_summary__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs

class JobOpening(models.Model):

    FIELD_CHOICES = [
        ('', 'Select Field'),
        ('Administration/Secretarial', 'Administration/Secretarial'),
        ('Agriculture/Agro-Allied', 'Agriculture/Agro-Allied'),
        ('Arts/Crafts/Languages', 'Arts/Crafts/Languages'),
        ('Aviation/Airline', 'Aviation/Airline'),
        ('Banking', 'Banking'),
        ('Building and Construction', 'Building and Construction'),
        ('Catering / Confectionery', 'Catering / Confectionery'),
        ('Consultancy', 'Consultancy'),
        ('Customer Care', 'Customer Care'),
        ('Education / Teaching', 'Education / Teaching'),
        ('Engineering / Technical', 'Engineering / Technical'),
        ('Finance/Accouting/Audit','Finance/Accouting/Audit'),
        ('General', 'General'),
        ('Graduate Jobs', 'Graduate Jobs'),
        ('Hospitality/Hotel/Restaurant', 'Hospitality/Hotel/Restaurant'),
        ('Human Resources', 'Human Resources'),
        ('Insurance', 'Insurance'),
        ('ICT/Computer', 'ICT/Computer'),
        ('Internships / Volunteering', 'Internships / Volunteering'),
        ('Janitorial Services', 'Janitorial Services'),
        ('Law / Legal', 'Law/Legal'),
        ('Logistics','Logistics'),
        ('Manutacturing', 'Manufacturing'),
        ('Media/ Advertising/ Branding', 'Media/ Advertising/ Branding'),
        ('Medical/Healthcare', 'Medical/Healthcare'),
        ('NGO/Non-Profit','NGO/Non-Profit'),
        ('Oil and Gas / Energy','Oil and Gas / Energy'),
        ('Pharmaceutical', 'Pharmaceutical'),
        ('Procurement / Store-keeping / Supply Chain', 'Procurement / Store-keeping / Supply Chain'),
        ('Project Management','Project Management'),
        ('Real Estate', 'Real Estate'),
        ('Research / Data Analysis', 'Research / Data Analysis'),
        ('Safety and Environment / HSE', 'Safety and Environment / HSE'),
        ('Sales / Marketing / Retail / Business Development', 'Sales / Marketing / Retail / Business Development'),
        ('Security Intelligence', 'Security Intelligence'),
        ('Transportation and Driving', 'Transportation and Driving'),
        ('Travel and Tours', 'Travel and Tours'),
    ]

    INDUSTRY_CHOICES = [
        ('', 'Select Industry'),
        ('Advertising / Branding / PR', 'Advertising / Branding / PR'),
        ('Agriculture / Agro-Allied', 'Agriculture / Agro-Allied'),
        ('Any','Any'),
        ('Aviation / Airline', 'Aviation / Airline'),
        ('Banking / Financial Services', 'Banking / Financial Services'),
        ('Building / Construction', 'Building / Construction'),
        ('Consulting', 'Consulting'),
        ('Creative / Arts','Creative / Arts'),
        ('Education / Teaching','Education / Teaching'),
        ('Engineering / Technical', 'Engineering / Technical'),
        ('Food Services', 'Food Services'),
        ('General', 'General'),
        ('Government', 'Government'),
        ('Healthcare / Medical', 'Healthcare / Medical'),
        ('Hospitality', 'Hospitality'),
        ('ICT / Telecommunication', 'ICT / Telecommunication'),
        ('Insurance', 'Insurance'),
        ('Janitorial Services / Environment', 'Janitorial Services / Environment'),
        ('Law / Legal', 'Law / Legal'),
        ('Logistics and Transportation', 'Logistics and Transportation'),
        ('Manufacturing / Production / FMCG', 'Manufacturing / Production / FMCG'),
        ('Media / Radio / TV','Media / Radio / TV'),
        ('NGO / Non-Profit Associations', 'NGO / Non-Profit Associations'),
        ('Oil and Gas / Marine', 'Oil and Gas / Marine'),
        ('Online Sales / Marketing', 'Online Sales / Marketing'),
        ('Pharmaceuticals', 'Pharmaceuticals'),
        ('Power / Energy', 'Power / Energy'),
        ('Professional / Social Associations', 'Professional / Social Associations'),
        ('Real Estate', 'Real Estate'),
        ('Religious', 'Religious'),
        ('Sales / Retail', 'Sales / Retail'),
        ('Security', 'Security'),
        ('Travel and Tours', 'Travel and Tours'),
    ]

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

    EXPERIENCE_CHOICES = [
        ('', 'Select Experience Required'),
        ('1-4 years', '1-4 years'),
        ('5-10 years', '5-10 years'),
        ('11-35 years', '11-35 years')
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

    JOB_TYPE_CHOICES = [
        ('Full Time', 'Full Time'),
        ('Contract', 'Contract')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=140)
    job_summary = models.TextField()
    job_description = models.TextField()
    company_name = models.CharField(max_length=140)
    saved = models.ManyToManyField(User, related_name='saved_job', blank=True)
    job_type = models.CharField(choices=JOB_TYPE_CHOICES, max_length=30)
    company_email = models.EmailField(max_length=254)
    method_of_application = models.TextField(blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    experience = models.CharField(choices=EXPERIENCE_CHOICES, max_length=20)
    field = models.CharField(choices=FIELD_CHOICES, max_length=140)
    state = models.CharField(max_length=140)
    education = models.CharField(choices=EDUCATION_CHOICES, max_length=140)
    industry = models.CharField(choices=INDUSTRY_CHOICES, max_length=140)
    send_cv_directly = models.BooleanField(default=False)
    objects = JobManager()
    
    def __str__(self):
        return '{} - {}'.format(self.user, self.job_title)

    def get_absolute_url(self):
        return reverse('job-detail', kwargs={'pk': self.pk})

    def get_api_save_job_url(self):
        return reverse("save-job-api-toggle", kwargs={'pk': self.pk})
    
    def get_save_job_url(self):
        return reverse("save-job-toggle", kwargs={'pk': self.pk})
    
        
class ShareJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(JobOpening, on_delete=models.CASCADE)
    content = models.TextField(validators=[validate_is_profane], null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='share_job_likes', blank=True)
    image = models.ImageField(upload_to='shared_pic/', blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    is_quote = models.BooleanField(default=False)
    share_post = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    
    def get_absolute_url(self):
        return reverse('job-thread', kwargs={'pk': self.job.pk})

    def __str__(self):
        return '{}- {}'.format(self.job.job_title, str(self.user.username))    

    def get_like_url(self):
        return reverse("share-job-like-toggle", kwargs={'pk': self.pk})
    
    def get_api_like_url(self):
        return reverse("share-job-like-api-toggle", kwargs={'pk': self.pk})        


class RequestJob(models.Model):
    
    FIELD_CHOICES = [
        ('', 'Select Field'),
        ('Administration/Secretarial', 'Administration/Secretarial'),
        ('Agriculture/Agro-Allied', 'Agriculture/Agro-Allied'),
        ('Arts/Crafts/Languages', 'Arts/Crafts/Languages'),
        ('Aviation/Airline', 'Aviation/Airline'),
        ('Banking', 'Banking'),
        ('Building and Construction', 'Building and Construction'),
        ('Catering / Confectionery', 'Catering / Confectionery'),
        ('Consultancy', 'Consultancy'),
        ('Customer Care', 'Customer Care'),
        ('Education / Teaching', 'Education / Teaching'),
        ('Engineering / Technical', 'Engineering / Technical'),
        ('Finance/Accouting/Audit','Finance/Accouting/Audit'),
        ('General', 'General'),
        ('Graduate Jobs', 'Graduate Jobs'),
        ('Hospitality/Hotel/Restaurant', 'Hospitality/Hotel/Restaurant'),
        ('Human Resources', 'Human Resources'),
        ('Insurance', 'Insurance'),
        ('ICT/Computer', 'ICT/Computer'),
        ('Internships / Volunteering', 'Internships / Volunteering'),
        ('Janitorial Services', 'Janitorial Services'),
        ('Law / Legal', 'Law/Legal'),
        ('Logistics','Logistics'),
        ('Manutacturing', 'Manufacturing'),
        ('Media/ Advertising/ Branding', 'Media/ Advertising/ Branding'),
        ('Medical/Healthcare', 'Medical/Healthcare'),
        ('NGO/Non-Profit','NGO/Non-Profit'),
        ('Oil and Gas / Energy','Oil and Gas / Energy'),
        ('Pharmaceutical', 'Pharmaceutical'),
        ('Procurement / Store-keeping / Supply Chain', 'Procurement / Store-keeping / Supply Chain'),
        ('Project Management','Project Management'),
        ('Real Estate', 'Real Estate'),
        ('Research / Data Analysis', 'Research / Data Analysis'),
        ('Safety and Environment / HSE', 'Safety and Environment / HSE'),
        ('Sales / Marketing / Retail / Business Development', 'Sales / Marketing / Retail / Business Development'),
        ('Security Intelligence', 'Security Intelligence'),
        ('Transportation and Driving', 'Transportation and Driving'),
        ('Travel and Tours', 'Travel and Tours'),
    ]

    INDUSTRY_CHOICES = [
        ('', 'Select Industry'),
        ('Advertising / Branding / PR', 'Advertising / Branding / PR'),
        ('Agriculture / Agro-Allied', 'Agriculture / Agro-Allied'),
        ('Any','Any'),
        ('Aviation / Airline', 'Aviation / Airline'),
        ('Banking / Financial Services', 'Banking / Financial Services'),
        ('Building / Construction', 'Building / Construction'),
        ('Consulting', 'Consulting'),
        ('Creative / Arts','Creative / Arts'),
        ('Education / Teaching','Education / Teaching'),
        ('Engineering / Technical', 'Engineering / Technical'),
        ('Food Services', 'Food Services'),
        ('General', 'General'),
        ('Government', 'Government'),
        ('Healthcare / Medical', 'Healthcare / Medical'),
        ('Hospitality', 'Hospitality'),
        ('ICT / Telecommunication', 'ICT / Telecommunication'),
        ('Insurance', 'Insurance'),
        ('Janitorial Services / Environment', 'Janitorial Services / Environment'),
        ('Law / Legal', 'Law / Legal'),
        ('Logistics and Transportation', 'Logistics and Transportation'),
        ('Manufacturing / Production / FMCG', 'Manufacturing / Production / FMCG'),
        ('Media / Radio / TV','Media / Radio / TV'),
        ('NGO / Non-Profit Associations', 'NGO / Non-Profit Associations'),
        ('Oil and Gas / Marine', 'Oil and Gas / Marine'),
        ('Online Sales / Marketing', 'Online Sales / Marketing'),
        ('Pharmaceuticals', 'Pharmaceuticals'),
        ('Power / Energy', 'Power / Energy'),
        ('Professional / Social Associations', 'Professional / Social Associations'),
        ('Real Estate', 'Real Estate'),
        ('Religious', 'Religious'),
        ('Sales / Retail', 'Sales / Retail'),
        ('Security', 'Security'),
        ('Travel and Tours', 'Travel and Tours'),
    ]

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

    EXPERIENCE_CHOICES = [
        ('', 'Select Experience Required'),
        ('1-4 years', '1-4 years'),
        ('5-10 years', '5-10 years'),
        ('11-35 years', '11-35 years')
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

    JOB_TYPE_CHOICES = [
        ('Full Time', 'Full Time'),
        ('Contract', 'Contract')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_type = models.CharField(choices=JOB_TYPE_CHOICES, max_length=45)
    field = models.CharField(choices=FIELD_CHOICES, max_length=100)
    industry = models.CharField(choices=INDUSTRY_CHOICES, max_length=140)
    state = models.CharField(choices=STATE_CHOICES, max_length=20)
    education = models.CharField(choices=EDUCATION_CHOICES, max_length=45)
    experience = models.CharField(choices=EXPERIENCE_CHOICES, max_length=20)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{} - {}'.format(self.user, self.field)

    def get_absolute_url(self):
        return reverse('all_jobs')
        # return reverse('job-detail', kwargs={'pk': self.pk})
