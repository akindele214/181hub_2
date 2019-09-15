# Generated by Django 2.2.4 on 2019-09-13 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0013_jobopening_saved'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobopening',
            name='job_summary',
            field=models.TextField(default='Coordinate development and implementation of policy and procurement strategies for spends across the organisation in accordance with agreed annual performance targets. Manage technical inventory management activities of the company'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='jobopening',
            name='experience',
            field=models.CharField(choices=[('', 'Select Experience Required'), ('1-4 years', '1-4 years'), ('5-10 years', '5-10 years'), ('11-35 years', '11-35 years')], max_length=20),
        ),
        migrations.AlterField(
            model_name='jobopening',
            name='field',
            field=models.CharField(choices=[('', 'Select Field'), ('Administration/Secretarial', 'Administration/Secretarial'), ('Agriculture/Agro-Allied', 'Agriculture/Agro-Allied'), ('Arts/Crafts/Languages', 'Arts/Crafts/Languages'), ('Aviation/Airline', 'Aviation/Airline'), ('Banking', 'Banking'), ('Building and Construction', 'Building and Construction'), ('Catering / Confectionery', 'Catering / Confectionery'), ('Consultancy', 'Consultancy'), ('Customer Care', 'Customer Care'), ('Education / Teaching', 'Education / Teaching'), ('Engineering / Technical', 'Engineering / Technical'), ('Finance/Accouting/Audit', 'Finance/Accouting/Audit'), ('General', 'General'), ('Graduate Jobs', 'Graduate Jobs'), ('Hospitality/Hotel/Restaurant', 'Hospitality/Hotel/Restaurant'), ('Human Resources', 'Human Resources'), ('Insurance', 'Insurance'), ('ICT/Computer', 'ICT/Computer'), ('Internships / Volunteering', 'Internships / Volunteering'), ('Janitorial Services', 'Janitorial Services'), ('Law / Legal', 'Law/Legal'), ('Logistics', 'Logistics'), ('Manutacturing', 'Manufacturing'), ('Media/ Advertising/ Branding', 'Media/ Advertising/ Branding'), ('Medical/Healthcare', 'Medical/Healthcare'), ('NGO/Non-Profit', 'NGO/Non-Profit'), ('Oil and Gas / Energy', 'Oil and Gas / Energy'), ('Pharmaceutical', 'Pharmaceutical'), ('Procurement / Store-keeping / Supply Chain', 'Procurement / Store-keeping / Supply Chain'), ('Project Management', 'Project Management'), ('Real Estate', 'Real Estate'), ('Research / Data Analysis', 'Research / Data Analysis'), ('Safety and Environment / HSE', 'Safety and Environment / HSE'), ('Sales / Marketing / Retail / Business Development', 'Sales / Marketing / Retail / Business Development'), ('Security Intelligence', 'Security Intelligence'), ('Transportation and Driving', 'Transportation and Driving'), ('Travel and Tours', 'Travel and Tours')], max_length=140),
        ),
        migrations.AlterField(
            model_name='jobopening',
            name='industry',
            field=models.CharField(choices=[('', 'Select Industry'), ('Advertising / Branding / PR', 'Advertising / Branding / PR'), ('Agriculture / Agro-Allied', 'Agriculture / Agro-Allied'), ('Any', 'Any'), ('Aviation / Airline', 'Aviation / Airline'), ('Banking / Financial Services', 'Banking / Financial Services'), ('Building / Construction', 'Building / Construction'), ('Consulting', 'Consulting'), ('Creative / Arts', 'Creative / Arts'), ('Education / Teaching', 'Education / Teaching'), ('Engineering / Technical', 'Engineering / Technical'), ('Food Services', 'Food Services'), ('General', 'General'), ('Government', 'Government'), ('Healthcare / Medical', 'Healthcare / Medical'), ('Hospitality', 'Hospitality'), ('ICT / Telecommunication', 'ICT / Telecommunication'), ('Insurance', 'Insurance'), ('Janitorial Services / Environment', 'Janitorial Services / Environment'), ('Law / Legal', 'Law / Legal'), ('Logistics and Transportation', 'Logistics and Transportation'), ('Manufacturing / Production / FMCG', 'Manufacturing / Production / FMCG'), ('Media / Radio / TV', 'Media / Radio / TV'), ('NGO / Non-Profit Associations', 'NGO / Non-Profit Associations'), ('Oil and Gas / Marine', 'Oil and Gas / Marine'), ('Online Sales / Marketing', 'Online Sales / Marketing'), ('Pharmaceuticals', 'Pharmaceuticals'), ('Power / Energy', 'Power / Energy'), ('Professional / Social Associations', 'Professional / Social Associations'), ('Real Estate', 'Real Estate'), ('Religious', 'Religious'), ('Sales / Retail', 'Sales / Retail'), ('Security', 'Security'), ('Travel and Tours', 'Travel and Tours')], max_length=140),
        ),
    ]
