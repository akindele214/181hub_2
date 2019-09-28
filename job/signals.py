from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import RequestJob, JobOpening
from blog.models import Post
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, send_mail
from notifications.signals import notify

# @receiver(post_save, sender=JobOpening)
# def after_job_create(sender, instance, created, **kwargs):
#     if created:
#         print('555')

# @receiver(post_save, sender=JobOpening)
# def save_post(sender, instance, **kwargs):
#     print('555')

# post_save.connect(after_job_create, sender=JobOpening)


@receiver(post_save, sender=JobOpening)
def after_job_create(sender, instance, created, **kwargs):
    accuracy = 0
    all_request = RequestJob.objects.all()
    if created:
        print("job Saved", instance)
        print("JOb SAVED")
        for req in all_request:
            if req.field == instance.field:
                accuracy += .1                
            else:
                pass
            if req.industry == instance.industry:
                accuracy += .1                
            else:
                pass
            if req.job_type == instance.job_type:
                accuracy += .1                
            else:
                pass
            if req.education == instance.education:
                accuracy += .1                
            else: 
                pass
            if req.experience == instance.experience:
                accuracy += .05
            else:
                pass
            if req.state == instance.state:
                accuracy += .05
            else:
                pass                
            accuracy_percentage = int(accuracy/.5 * 100)
            if accuracy_percentage >=50 and req.user != instance.user:
                subject = 'Job Request Match'
                body  = '{} posted a job that matches your request by {}{}, click the link to check it out https://181hub.com/job/{}/detail . Regards'.format(str(instance.user.username), str(accuracy_percentage),'%', str(instance.pk))
                print(subject, body)
                notify.send(instance.user, recipient=req.user,
                            verb="posted a job that matches your request by {}{}".format(accuracy_percentage,"%"), 
                            action_object=instance)
                email = send_mail(
                'Job Request Notification', 
                body,
                '181hub@gmail.com',
                [req.user.email],
                fail_silently= True)                
                print('A new job posted by',instance.user, 'matches', req.user.username+"'s", 'job request by', accuracy_percentage)
            accuracy = 0

                


# @receiver(post_save, sender=JobOpening)
# def save_post(sender, instance, **kwargs):
#     print("JOb SAVED")
#     accuracy = 0
#     all_request = RequestJob.objects.all()
#     for req in all_request:
#         if req.field == instance.field:
#             accuracy += .3
#             print("State Match", accuracy)
#         else:
#             pass

post_save.connect(after_job_create, sender=JobOpening)