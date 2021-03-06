from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, reverse
from django.views.generic import ListView, View, CreateView, UpdateView, DeleteView, RedirectView, DetailView
from .models import JobOpening, ShareJob, RequestJob
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CreateJobForm, CreateShareForm, ShareJobEditForm, QuoteJobForm
from django.contrib import messages
from notifications.signals import notify
from notifications.models import Notification
# REST FRAMEWORK
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

# Create your views here.

class AllJobs(ListView):    
    ordering = ['-date_posted']
    context_object_name = 'posts'
    paginate_by = 30
    template_name = 'job/job_home.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['model'] = self.model
        return context
    
    def get_queryset(self):
        posts = JobOpening.objects.all().order_by('-date_posted')
        return posts    

class CreateJobOpening(LoginRequiredMixin, CreateView):
    model = JobOpening

    def get(self, request):
        form = CreateJobForm()
        context = {
            'form': form,
        }
        return render(request, 'job/job_create_form.html', context)
    
    def post(self, request):
        if request.method == 'POST':
            form = CreateJobForm(request.POST or None)
            if form.is_valid():
                print('Valid Form')
                job_title = form.cleaned_data['job_title']
                method_of_application = form.cleaned_data['method_of_application']
                field = form.cleaned_data['field']
                education = form.cleaned_data['education']
                industry = form.cleaned_data['industry']
                job_description = form.cleaned_data['job_description']
                company_description = form.cleaned_data['company_description']
                send_cv_directly = form.cleaned_data['send_cv_directly']
                experience = form.cleaned_data['experience']
                job_type = form.cleaned_data['job_type']
                state = form.cleaned_data['state']
                company_name = form.cleaned_data['company_name']

                job_create =  JobOpening.objects.create(user= request.user, 
                                                        job_title= job_title, 
                                                        job_description= job_description, 
                                                        company_description= company_description,
                                                        company_name=company_name,
                                                        industry= industry, 
                                                        field= field, 
                                                        education= education, 
                                                        experience=experience,
                                                        send_cv_directly=send_cv_directly,
                                                        job_type=job_type,
                                                        method_of_application= method_of_application,
                                                        state=state
                                                        )
                job_create.save()            
                return redirect('all_jobs')
            else:
                print(form.non_field_errors)
                print('Invalid form')    
        else:

            form = CreateJobForm()

        context = {
            'form': form 
        }
        return render(request, 'job/job_create_form.html', context)

class JobDetail(DetailView):

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        UserId = request.user.id
        post = get_object_or_404(JobOpening, pk=pk)

        # comment_form = CommentForm()
        # comments = Comment.objects.filter(post__exact=post, reply=None).order_by('-id')
        is_liked = False
        is_saved = False
        is_thread = False

        # if Share.objects.filter(post__exact=pk).exists():
        #     is_thread = True

        # if UserId in post.likes.all():
        #     is_liked = True

        if request.user in post.saved.all():
            is_saved = True 
        context = {
            'object': post,
            'is_thread': is_thread,
            'is_liked': is_liked,
            # 'total_likes': post.total_likes(),
            # 'comments': comments,
            # 'comment_form': comment_form,
            'is_saved': is_saved,

        }
        return render(request, 'job/job_detail.html', context)    

class JobUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = JobOpening
    fields = [
              'job_title',
              'job_description',
              'company_description',
              'company_name',
              'job_type',
              'education',
              'industry',
              'field',
              'state',
              'company_email',
              'experience',
              'method_of_application',
              'send_cv_directly',
             ]
    template_name = 'blog/postupdate.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

class DeleteJobView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = JobOpening
    # success_url = reverse('all_jobs')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        user = post.user
        notifications = Notification.objects.filter(action_object_content_type__model= 'jobopening', action_object_object_id=post.pk)
        for notification in notifications.all():
            if int(notification.action_object_object_id) == post.id:
                notification.delete()
            else:
                pass
        post.delete()
        return redirect('all_jobs')

class SaveJobToggle(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        post = get_object_or_404(JobOpening, pk=pk)
        url_ = post.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in post.saved.all():
                post.saved.remove(user)
            else:
                post.saved.add(user)
        return url_

class SaveJobAPIToggle(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None, format=None):
        post = get_object_or_404(JobOpening, pk=pk)
        is_saved = False
        updated = False
        url_ = post.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in post.saved.all():
                post.saved.remove(user)
                is_saved = False
            else:
                post.saved.add(user)
                is_saved = True
            updated = True
        data = {
            'updated': updated,
            'is_saved': is_saved
        }
        return Response(data)

class ShareJobView(LoginRequiredMixin, CreateView):
    model = ShareJob
    # fields = ['content', 'post', 'user']
    template_name = 'job/job_share.html'
    success_url = '/'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        form = CreateShareForm()
        post = get_object_or_404(JobOpening, pk=pk)
        context = {
            'form': form,
            'post': post,
        }
        return render(request, 'job/job_share.html', context)

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        post = get_object_or_404(JobOpening, pk=pk)
        if request.method == 'POST':
            share_form = CreateShareForm(request.POST or None, request.FILES or None)
            if share_form.is_valid():
                image = share_form.cleaned_data['image']  # request.POST.get('image')
                content = share_form.cleaned_data['content']
                post_id = pk
                share_create = ShareJob.objects.create(job=post, user=request.user, content=content, image=image)
                share_create.save()
                # for word in content.split():
                #     if len(word) > 1:
                #         if word.startswith("#"):
                #             wo = word.replace('#', '')
                #             hash_tag = ShareTag(share=share_create, tag=wo, user=request.user)
                #             hash_tag.save()
                # for word in content.split():
                #     if word.startswith("@"):
                #         w = word.replace('@', '')
                #         if User.objects.get(username__iexact=w): 
                #             notify.send(request.user, recipient=User.objects.get(username__iexact=w),
                #                         verb='mentioned you in a post thread', action_object=post, description=content)
                #         else:
                #             pass
            messages.success(request, f'Job Shared')
            return redirect('job-thread', pk=pk)
        else:
            form = ShareJob()
        context = {
            'post': post,
            'form': form,
        }

        return render(request, 'job/job_share.html', context)   

class ShareJobUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView, RedirectView):
    model = ShareJob
    # fields = ['content', 'image']
    # template_name = 'blog/share_update.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        share = self.get_object()
        if self.request.user == share.user:
            return True
        return False

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        share = ShareJob.objects.get(pk=pk)
        share_username = '@'+share.user.username
        form = ShareJobEditForm(instance=share, initial={'content': share_username})
        context = {
            'form': form,
            'post': share,
        }
        return render(request, 'blog/share_update.html', context)

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        share = ShareJob.objects.get(pk=pk)
        form = ShareJobEditForm(instance=share)
        prev_mentions = []
        prev_hashtags = []
        new_mentions = []
        new_hashtags = []
        prev_post = ShareJobEditForm(instance=share)
        prev_content = prev_post['content'].value()
        for word in prev_content.split():
            if word.startswith("@"):
                prev_mentions.append(word)
        for word in prev_content.split():
            if word.startswith("#"):
                prev_hashtags.append(word)
        if request.method == 'POST':
            form = ShareJobEditForm(request.POST or None, request.FILES or None, instance=share) 
            if form.is_valid():
                content = form.cleaned_data['content']
                new_content = form['content'].value()
                for word in new_content.split():
                    if word.startswith("@"):
                        new_mentions.append(word)
                for word in new_content.split():
                    if word.startswith("#"):
                        new_hashtags.append(word)
                form.save()
                diff_hastags = list(set(new_hashtags) - set(prev_hashtags))
                diff_mentions = list(set(new_mentions) - set(prev_mentions))
                # if len(diff_mentions) >= 1:
                #     for word in diff_mentions:
                #         if word.startswith("@"):
                #             w = word.replace('@', '')
                #             try:
                #                 if User.objects.get(username__iexact=w):
                #                     if request.user != User.objects.get(username__iexact=w):
                #                         notify.send(request.user, recipient=User.objects.get(username__iexact=w), verb='mentioned you in a post thread', action_object=share.post, description=content)
                #             except User.DoesNotExist:
                #                 pass
                # if len(diff_hastags) >= 1:
                #     del_hash = ShareTag.objects.filter(share__exact=pk)
                #     del_hash.delete()                    
                #     for word in new_hashtags:
                #         if word.startswith("#"):
                #             wo = word.replace('#', '')
                #             hash_tag = ShareTag(share=share, tag=wo, user= request.user)
                #             hash_tag.save()
                return HttpResponseRedirect(reverse('job-thread', kwargs={'pk': share.job.id}))
        else:
            form = ShareJobEditForm(instance=share)

        context = {
            'form': form,
            'share': share,
        }
        return HttpResponseRedirect(share.get_absolute_url())

    def get_success_url(self):
        return reverse('share-thread', kwargs={'pk': self.object.post.id})

class DeleteShareJob(LoginRequiredMixin, UserPassesTestMixin, DeleteView, RedirectView):
    model = ShareJob
    template_name = 'job/share_confirm_delete.html'
    context_object_name = "share"
    

    def test_func(self):
        share = self.get_object()
        if self.request.user == share.user:
            return True
        return False
    
    # def delete(self):


    def get_success_url(self):
        return reverse('job-thread', kwargs={'pk': self.object.job.pk})

class ShareJobThread(ListView):
    model = ShareJob
    paginate_by = 30
    context_object_name = 'shares'
    template_name = 'job/job_thread.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['post_id'] = self.request.GET.get('pk')
        context['ori_post'] = JobOpening.objects.get(pk=self.kwargs.get('pk'))
        return context

    def get_queryset(self):
        post_id = self.kwargs.get('pk')
        shares = ShareJob.objects.filter(job__exact=post_id)
        share = shares.order_by('date_posted')
        return share    
    
class LikeShareJobToggle(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        print(pk)
        obj = get_object_or_404(ShareJob, pk=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_    

class LikeShareApiToggle(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only authenticated users are able to access this view.
    """
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None, format=None):
        # pk = self.kwargs.get('pk')
        obj = get_object_or_404(ShareJob, pk=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user
        updated = False
        liked = False

        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
                liked = False
            else:
                obj.likes.add(user)
                liked = True
                # sif request.user != obj.user:
                #     notify.send(request.user, recipient=obj.user, verb='liked your post in a thread', action_object=obj.post,description=obj.content)
            updated = True
        data = {
            "updated": updated,
            "liked": liked,
            "like_count": obj.likes.count()
        }
        return Response(data)

class QuoteJobShare(LoginRequiredMixin, CreateView):

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        form = QuoteJobForm()
        share_post = get_object_or_404(ShareJob, pk=pk)
        context = {
            'form': form,
            'share_post': share_post, 
        }
        return render(request, 'blog/quote.html', context)
    
    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        share_post = get_object_or_404(ShareJob, pk=pk)
        if request.method == 'POST':
            quote_form = QuoteJobForm(request.POST or None, request.FILES or None)
            if quote_form.is_valid():
                image = quote_form.cleaned_data['image']
                content = quote_form.cleaned_data['content']
                share_pk = pk
                quote_create = ShareJob.objects.create(job=share_post.job, share_post=share_post, is_quote=True, user=request.user, content = content, image=image)
                quote_create.save()

                # for word in content.split():
                #     if len(word) > 1:
                #         if word.startswith("#"):
                #             wo = word.replace('#', '')
                #             hash_tag = ShareTag(share=quote_create, tag=wo, user=request.user)
                #             hash_tag.save()
                # for word in content.split():
                #     if word.startswith("@"):
                #         w = word.replace('@', '')
                #         if User.objects.get(username__iexact=w):
                #             notify.send(request.user, recipient=User.objects.get(username__iexact=w),
                #                         verb='mentioned you in a post thread', action_object=share_post.post, description=content)
                #         else:
                #             pass

            messages.success(request, f'Done')
            return redirect('job-thread', pk=share_post.job.pk)
        else:
            form = QuoteJobForm()
        context = {
            'form': form,
            'share_post': share_post
        }
        return render(request, 'blog/quote.html', context)

class RequestJobCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = RequestJob
    template_name = 'job/request_job.html'
    fields = ['job_type', 'field', 'industry', 'education', 'state', 'experience']
    success_message = "Request Submitted, You'll Be Notified When A Job That Matches Your Specification Is In The Database"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class RequestJobList(LoginRequiredMixin, ListView):
    model =  RequestJob
    template_name = 'job/request_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        posts = RequestJob.objects.filter(user__exact=self.request.user).order_by('-date_posted')
        return posts      

class RequestDeleteView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, DeleteView):
    model = RequestJob
    template_name = 'job/request_confirm_delete.html'
    context_object_name = "share"

    def test_func(self):
        share = self.get_object()
        if self.request.user == share.user:
            return True
        return False

    def get_success_url(self):
        messages.success(self.request, 'Your Job Request Has Been Deleted')
        return reverse('request-list')
