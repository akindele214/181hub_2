from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone 
# Create your models here.

class JobOpening(models.Model):

    FIELD_CHOICES = [
        ('', 'Select Field'),
        ('admin', 'Administration/Secretarial'),
        ('agric', 'Agriculture/Agro-Allied'),
        ('arts/crafts/languages', 'Arts/Crafts/Languages'),
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
        ('HR', 'Human Resources'),
        ('Insurance', 'Insurance'),
        ('ICT', 'ICT/Computer'),
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
        ('any','Any'),
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
        ('1-4', '1-4 years'),
        ('5-10', '5-10 years'),
        ('11-35', '11-35 years')
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=140)
    job_description = models.TextField()
    method_of_application = models.TextField(blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    experience = models.CharField(choices=EXPERIENCE_CHOICES, max_length=20)
    image = models.ImageField(upload_to='company_pic/', blank=True, null=True)
    field = models.CharField(choices=FIELD_CHOICES, max_length=140)
    state = models.CharField(max_length=20)
    education = models.CharField(max_length=140)
    industry = models.CharField(choices=INDUSTRY_CHOICES, max_length=140)
    send_cv_directly = models.BooleanField(default=False)
    
    def __str__(self):
        return '{} - {}'.format(self.user, self.job_title)