# Generated by Django 2.2.4 on 2019-09-11 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0006_jobopening_experience'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobopening',
            name='state',
            field=models.CharField(choices=[('Abia', 'Abia'), ('Abuja', 'Abuja'), ('Adamawa', 'Adamawa'), ('Akwa Ibom', 'Akwa Ibom'), ('Anambra', 'Anambra'), ('Bauchi', 'Bauchi'), ('Bayelsa', 'Bayelsa'), ('Benue', 'Benue'), ('Borno', 'Borno'), ('Cross River', 'Cross River'), ('Delta', ' Delta'), ('Ebonyi', 'Ebonyi'), ('Edo', 'Edo'), ('Ekiti', 'Ekiti'), ('Enugu', 'Enugu'), ('Gombe', 'Gombe'), ('Imo', 'Imo'), ('Jigawa', 'Jigawa'), ('Kaduna', 'Kaduna'), ('Kano', 'Kano'), ('Katsina', 'Katsina'), ('Kebbi', 'Kebbi'), ('Kogi', 'Kogi'), ('Kwara', 'Kwara'), ('Lagos', 'Lagos'), ('Nasarawa', 'Nasawara'), ('Niger', 'Niger'), ('Ogun', 'Ogun'), ('Ondo', 'Ondo'), ('Osun', 'Osun'), ('Other', 'Other'), ('Oyo', 'Oyo'), ('Plateau', 'Plateau'), ('Rivers', 'Rivers'), ('Sokoto', 'Sokoto'), ('Taraba', 'Taraba'), ('Yobe', 'Yobe'), ('Zamfara', 'Zamfara')], default='Lagos', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='jobopening',
            name='industry',
            field=models.CharField(choices=[('', 'Select Industry'), ('Advertising / Branding / PR', 'Advertising / Branding / PR'), ('Agriculture / Agro-Allied', 'Agriculture / Agro-Allied'), ('any', 'Any'), ('Aviation / Airline', 'Aviation / Airline'), ('Banking / Financial Services', 'Banking / Financial Services'), ('Building / Construction', 'Building / Construction'), ('Consulting', 'Consulting'), ('Creative / Arts', 'Creative / Arts'), ('Education / Teaching', 'Education / Teaching'), ('Engineering / Technical', 'Engineering / Technical'), ('Food Services', 'Food Services'), ('General', 'General'), ('Government', 'Government'), ('Healthcare / Medical', 'Healthcare / Medical'), ('Hospitality', 'Hospitality'), ('ICT / Telecommunication', 'ICT / Telecommunication'), ('Insurance', 'Insurance'), ('Janitorial Services / Environment', 'Janitorial Services / Environment'), ('Law / Legal', 'Law / Legal'), ('Logistics and Transportation', 'Logistics and Transportation'), ('Manufacturing / Production / FMCG', 'Manufacturing / Production / FMCG'), ('Media / Radio / TV', 'Media / Radio / TV'), ('NGO / Non-Profit Associations', 'NGO / Non-Profit Associations'), ('Oil and Gas / Marine', 'Oil and Gas / Marine'), ('Online Sales / Marketing', 'Online Sales / Marketing'), ('Pharmaceuticals', 'Pharmaceuticals'), ('Power / Energy', 'Power / Energy'), ('Professional / Social Associations', 'Professional / Social Associations'), ('Real Estate', 'Real Estate'), ('Religious', 'Religious'), ('Sales / Retail', 'Sales / Retail'), ('Security', 'Security'), ('Travel and Tours', 'Travel and Tours')], max_length=140),
        ),
    ]
