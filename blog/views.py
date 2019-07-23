from django.utils import timezone
import operator
from urllib.parse import urlencode
from django.contrib import messages
from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Post, Comment, Share, Images, HashTag, ShareTag, Quote, Report
from django.views.generic import ListView, View, CreateView, UpdateView, DeleteView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect, Http404  # HttpResponse, Http404
from django.db.models import Q
from django.template.loader import render_to_string
from .forms import CommentForm, ShareForm, PostCreateForm, PostEditForm, ShareEditForm, QuoteForm, ReportForm
from itertools import chain
from user.models import Profile
from notifications.signals import notify
from django.forms import modelformset_factory
from hitcount.views import HitCountDetailView
from hitcount.models import HitCount
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# REST FRAMEWORK
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User



# Create your views here.


def home(request):
    post = Post.objects.all()
    query = request.GET.get('q')
    if query:
        post = Post.objects.filter(
            Q(title__icontains=query) |
            Q(user__username=query) |
            Q(content__icontains=query)
        )

    context = {
        'posts': post
    }

    return render(request, 'blog/home.html', context)


'''class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    ordering = ['-date_posted']
    context_object_name = 'posts'
    paginate_by = 10'''


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    ordering = ['-date_posted']
    context_object_name = 'posts'
    paginate_by = 30

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['model'] = self.model
        return context

    def get_queryset(self):
        posts = []
        shared_post = []
        hash_post = []
        final_hash_post = []
        final_post = []
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
            view_user_post = Post.objects.filter(user__exact=self.request.user)
            user_profile = User.objects.get(id=user_id).profile

            date = timedelta(days=7)
            last_week = timezone.now() - date
            all_tag = HashTag.objects.filter(date_posted__gt=last_week).exclude(user=self.request.user).values_list('post', flat=True).distinct()

            for postx in all_tag:
                post_post = Post.objects.get(pk=postx)
                final_post.append(post_post)

            for profile in user_profile.follower.all():
                for post in Post.objects.filter(user__exact=profile.user):
                    posts.append(post)

            for profile in user_profile.follower.all():
                for share in Share.objects.filter(user__exact=profile.user):
                    shared_post.append(share)

            for f_post in final_post:
                if f_post.user.profile not in user_profile.follower.all():
                    final_hash_post.append(f_post)
            # logged_in_user_shared_post = Share.objects.filter(post__user=self.request.user)
            logged_in_user_shared_post = Share.objects.filter(user__exact=self.request.user.id)
            chain_qs = chain(posts, view_user_post, shared_post,logged_in_user_shared_post, final_hash_post)
            return sorted(chain_qs, key=lambda x: x.date_posted, reverse=True)

        else:
            posts = Post.objects.all().order_by('?')
            return posts

class Trending(ListView):
    context_object_name = 'posts'
    paginate_by = 30
    template_name = 'blog/trending.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['model'] = self.model
        return context
    
    def get_queryset(self):
        users = self.request.user 
        return Post.objects.filter(hit_count_generic__hits__gt=25).order_by('date_posted')

    # def get(self, request, *args, **kwargs):
    #     post = Post.objects.filter(hit_count_generic__gt=105)
    #     print(post.count())
    #     context = {
    #         'post':post
    #     }
    #     return render(request, 'blog/trending.html', context)


class SearchView(ListView): 
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 30
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)
        
        if len(query) > 2:
            blog_results = Post.objects.search(query)
            profile_results = Profile.objects.search(query)
            queryset_chain = chain(profile_results, blog_results)

            qs = sorted(queryset_chain, key=lambda instance: instance.pk,
                        reverse=True)
            self.count = len(qs)
            return qs
        return Post.objects.none()


class HashSearchView(ListView):
    paginate_by = 30
    context_object_name = 'posts'
    template_name = 'blog/HashSearch.html'
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.kwargs['hash']
        return context

    def get_queryset(self):
        request = self.request
        query = self.kwargs['hash'] 
        # hash_post = HashTag.objects.all()
        if query:
            posts = HashTag.objects.filter(
                Q(tag__icontains=query))
            share = ShareTag.objects.filter(
                Q(tag__exact=query))
            queryset_chain = chain(posts,
                                   share)

            qs = sorted(queryset_chain, key=lambda instance: instance.date_posted,
                        reverse=True)
            self.count = len(qs)
            return qs
        else:
            HashTag.objects.none()


'''
class MentionSearchView(ListView):
    paginate_by = 20
    context_object_name = 'posts'
    template_name = 'blog/MentionSearch.html'
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('username')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('username')
        # hash_post = HashTag.objects.all()
        try:
            if User.objects.get(username__iexact=query):
                posts = Post.objects.filter(user__icontain=query)
                return posts

             
        except User.DoesNotExist:
            pass
'''


class MentionSearchView(ListView):
    # model = Post
    # template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    # context_object_name = 'post'
    # paginate_by = 15

    def get(self, request, *args, **kwargs):
        # username = request.GET.get('username')
        username = kwargs['username']
        try:
            if User.objects.get(username__iexact=username):
                user = User.objects.get(username__iexact=username)
                profile_user_id = get_object_or_404(User, username__iexact=username).profile
                profile = User.objects.get(username__iexact=username).profile
                posts = Post.objects.filter(user__exact=user).order_by('-date_posted')
                is_user = False
                is_follow = False

                post = Post.objects.filter(user__exact=user).order_by('-date_posted')
                page = request.GET.get('page', 1)
                paginator = Paginator(post, 30)
                try:
                    post = paginator.page(page)
                except PageNotAnInteger:
                    post = paginator.page(1)
                except EmptyPage:
                    post = paginator.page(paginator.num_pages)

                # if request.user.is_authenticated():
                if request.user.is_anonymous:
                    v_user = None
                else:
                    v_user = User.objects.get(id=request.user.id).profile
                    if v_user == profile:
                        is_user = True
                    v_user = None

                if request.user.is_authenticated:
                    v_user2 = User.objects.get(id=request.user.id).profile.id
                    if profile_user_id.following.filter(id__iexact=v_user2).exists():
                        is_follow = True
                else:
                    v_user2 = None
                context = {
                    'post': post,
                    'posts': posts,
                    'user': user,
                    'is_following': is_follow,
                    'total_follower': profile.following.count(),
                    'total_following': profile.follower.count(),
                    'is_user': is_user,
                }
                return render(request, 'blog/MentionSearch.html', context)
        except User.DoesNotExist:
            user_doesnt_not_exist = "User Does Not Exist"
            is_exist = False
            context = {
                'respose': user_doesnt_not_exist,
                'is_exist': is_exist
            }
            return render(request, 'blog/MentionSearch.html', context)


class PostMixinDetailView(object):
    """
    Mixin to same us some typing.  Adds context for us!
    """
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostMixinDetailView, self).get_context_data(**kwargs)
        context['post_list'] = Post.objects.all()[:]
        context['post_views'] = ["ajax", "detail", "detail-with-count"]
        return context


class PostDetailView(PostMixinDetailView, HitCountDetailView):
    model = Post
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(PostDetailView, cls).as_view(**initkwargs)
        return ensure_csrf_cookie(view)

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        UserId = request.user.id
        post = get_object_or_404(Post, pk=pk)

        comment_form = CommentForm()
        comments = Comment.objects.filter(post__exact=post, reply=None).order_by('-id')
        is_liked = False
        is_saved = False
        is_thread = False

        if Share.objects.filter(post__exact=pk).exists():
            is_thread = True

        if post.likes.filter(id__exact=UserId).exists():
            is_liked = True

        if post.saved.filter(id__exact=UserId).exists():
            is_saved = True 
        context = {
            'object': post,
            'is_thread': is_thread,
            'is_liked': is_liked,
            'total_likes': post.total_likes(),
            'comments': comments,
            'comment_form': comment_form,
            'is_saved': is_saved,

        }
        return render(request, 'blog/post_detail.html', context)

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        post = get_object_or_404(Post, pk=pk)
        UserId = request.user.id
        comments = Comment.objects.filter(post__exact=post, reply=None).order_by('-id')
        is_liked = False
        is_saved = False
        is_thread = False

        if Share.objects.filter(post__exact=pk).exists():
            is_thread = True

        if post.likes.filter(id__exact=UserId).exists():
            is_liked = True

        if post.saved.filter(id__exact=UserId).exists():
            is_saved = True

        if request.method == 'POST':
            comment_form = CommentForm(request.POST or None)
            if comment_form.is_valid():
                content = request.POST.get('content')
                reply_id = request.POST.get('comment_id')
                comment_qs = None
                if reply_id:
                    comment_qs = Comment.objects.get(id=reply_id)
                comment = Comment.objects.create(post=post, user=request.user, content=content, reply=comment_qs)
                comment.save()
                if request.user != post.user:
                    notify.send(request.user, recipient=post.user, verb='commented on your post', action_object=post)
                # return HttpResponseRedirect(object.get_absolute_url())
        else:
            comment_form = CommentForm()
        context = {
            'object': post,
            'is_thread': is_thread,
            'is_liked': is_liked,
            'total_likes': post.total_likes(),
            'comments': comments,
            'comment_form': comment_form,
            'is_saved': is_saved,
        }
        if request.is_ajax():
            html = render_to_string('blog/comments.html', context, request=request)
            return JsonResponse({'form': html})
        return render(request, 'blog/post_detail.html', context)


def postdetail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    UserId = request.user.id
    comments = Comment.objects.filter(post=post, reply=None).order_by('-id')
    is_liked = False
    is_saved = False
    # hitcount.views.HitCountMixin.hit_count()

    if post.likes.filter(id=UserId).exists():
        is_liked = True

    if post.saved.filter(id=UserId).exists():
        is_saved = True

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            comment = Comment.objects.create(post=post, user=request.user, content=content, reply=comment_qs)
            comment.save()
            notify.send(request.user, recipient=post.user, verb='commented on your post', action_object=post)
            # return HttpResponseRedirect(object.get_absolute_url())
    else:
        comment_form = CommentForm()
    context = {
        'object': post,
        'is_liked': is_liked,
        'total_likes': post.total_likes(),
        'comments': comments,
        'comment_form': comment_form,
        'is_saved': is_saved,
    }
    if request.is_ajax():
        html = render_to_string('blog/comments.html', context, request=request)
        return JsonResponse({'form': html})
    return render(request, 'blog/post_detail.html', context)


def save_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    is_saved = False
    if post.saved.filter(id=request.user.id).exists():
        post.saved.remove(request.user)
        is_saved = False
    else:
        post.saved.add(request.user)
        is_saved = True
    context = {
        'is_saved': is_saved
    }
    return HttpResponseRedirect(post.get_absolute_url())


def saved_post_list(request):
    users = request.user
    # saved_post = users.saved.all()
    saved_post = Post.objects.filter(saved=users)
    # Post.objects.filter(user=user).order_by('-date_posted')
    context = {
        'saved_post': saved_post
    }

    return render(request, 'blog/saved_post_list.html', context)


class SavedPostListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'blog/saved_post_list.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'saved_post'
    paginate_by = 30

    def get_queryset(self):
        users = self.request.user 
        # users = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(saved__exact=users).order_by('-date_posted')


@login_required
def like_post(request):
    # post = get_object_or_404(Post, pk=request.POST.get('post_id'))
    post = get_object_or_404(Post, id=request.POST.get('id'))
    userid = request.user.id
    is_liked = False
    if post.likes.filter(id__iexact=userid).exists():
        post.likes.remove(userid)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
        if request.user != post.user:
            notify.send(request.user, recipient=post.user, verb='liked your post', action_object=post)

    context = {
        'object': post,
        'is_liked': is_liked,
        'total_likes': post.total_likes(),
    }
    # next = request.META.get('HTTP_REFERER', None) or '/'
    # return HttpResponseRedirect(next)
    # return HttpResponseRedirect(post.get_absolute_url())
    if request.is_ajax():
        html = render_to_string('blog/like_section.html', context, request=request)
        return JsonResponse({'form': html})

class PostLikeToggle(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        print(pk)
        obj = get_object_or_404(Post, pk=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

class PostLikeAPIToggle(APIView):
    
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None, format=None):
        # pk = self.kwargs.get('pk')
        obj = get_object_or_404(Post, pk=pk)
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
                if request.user != obj.user:
                    notify.send(request.user, recipient=obj.user, verb='liked your post', action_object=obj)
            updated = True
        data = {
            "updated": updated,
            "liked": liked,
            "like_count": obj.likes.count()
        }
        return Response(data)

class ShareLikeAPIToggle(APIView):
    
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only authenticated users are able to access this view.
    """
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None, format=None):
        # pk = self.kwargs.get('pk')
        obj = get_object_or_404(Share, pk=pk)
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
                if request.user != obj.user:
                    notify.send(request.user, recipient=obj.user, verb='liked your post in a thread', action_object=obj.post,description=obj.content)
            updated = True
        data = {
            "updated": updated,
            "liked": liked,
            "like_count": obj.likes.count()
        }
        return Response(data)

class ShareLikeToggle(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        print(pk)
        obj = get_object_or_404(Share, pk=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_



class UserPostListView(ListView):
    model = Post

    def get(self, request, *args, **kwargs):
        username = kwargs['username']
        user = get_object_or_404(User, username=username)
        profile_user_id = get_object_or_404(User, username=username).profile
        profile = User.objects.get(username=username).profile
        posts = Post.objects.filter(user=user).order_by('date_posted')
        # self.object_list = Post.objects.filter(user=user).order_by('-date_posted')
        is_user = False
        is_follow = False
        bio_length = len(user.profile.content)


        post = Post.objects.filter(user=user).order_by('date_posted')
        page = request.GET.get('page', 1)
        paginator = Paginator(post, 30)
        try:
            post = paginator.page(page)
        except PageNotAnInteger:
            post = paginator.page(1)
        except EmptyPage:
            post = paginator.page(paginator.num_pages)

        # if request.user.is_authenticated():
        if request.user.is_anonymous:
            v_user = None
        else:
            v_user = User.objects.get(id=request.user.id).profile
            if v_user == profile:
                is_user = True 
            v_user = None

        if request.user.is_authenticated:
            v_user2 = User.objects.get(id=request.user.id).profile.id
            if profile_user_id.following.filter(id=v_user2).exists():
                is_follow = True
        else:
            v_user2 = None

        context = {
            'post': post,
            'posts': posts,
            'user': user,
            'is_following': is_follow,
            'total_follower': profile.following.count(),
            'total_following': profile.follower.count(),
            'is_user': is_user,
            'len': bio_length
        }
        return render(request, 'blog/user_posts.html', context)


def user_post(request, username):
    user = get_object_or_404(User, username=username)
    profile_user_id = get_object_or_404(User, username=username).profile
    profile = User.objects.get(username=username).profile
    post = Post.objects.filter(user=user).order_by('-date_posted')
    is_user = False
    is_follow = False

    # if request.user.is_authenticated():
    if request.user.is_anonymous:
        v_user = None
    else:
        v_user = User.objects.get(id=request.user.id).profile
        if v_user == profile:
            is_user = True 
        v_user = None

    if request.user.is_authenticated:
        v_user2 = User.objects.get(id=request.user.id).profile.id
        if profile_user_id.following.filter(id=v_user2).exists():
            is_follow = True
    else:
        v_user2 = None

    context = {
        'post': post,
        'user': user,
        'is_following': is_follow,
        'total_follower': profile.following.count(),
        'total_following': profile.follower.count(),
        'is_user': is_user,
    }

    return render(request, 'blog/user_posts.html', context)


@login_required
def follow(request, user_id):
    profile_user_id = User.objects.get(id=user_id).profile  # get_object_or_404(User, id=user_id)
    v_user = User.objects.get(id=request.user.id).profile.id  # get_object_or_404(User, id=request.POST.get('user_id'))
    # profile_id = v_user
    profile_user_id_2 = User.objects.get(id=user_id).profile.id  # get_object_or_404(User, id=user_id)
    v_user_2 = User.objects.get(id=request.user.id).profile  # get_object_or_404(User, id=request.POST.get('user_id'))
    # profile_id = v_user
    user = User.objects.get(id=user_id)
    is_follow = False
    if profile_user_id.following.filter(id__iexact=v_user).exists():
        profile_user_id.following.remove(v_user)
        v_user_2.follower.remove(profile_user_id_2)
        is_follow = False

    else:
        profile_user_id.following.add(v_user)
        v_user_2.follower.add(profile_user_id_2)
        is_follow = True
        if request.user != user:
            notify.send(request.user, recipient=user, verb='followed you')

    next_page = request.META.get('HTTP_REFERER', None) or '/'
    return HttpResponseRedirect(next_page)


def view_followers(request, username):
    profile_user_id = get_object_or_404(User, username=username).profile
    follower_list = profile_user_id.following.all()
    '''
        profile_user_id = get_object_or_404(User, username=username).profile
        v_user = User.objects.get(id=request.user.id).profile
        v_user2 = User.objects.get(id=request.user.id).profile.id
        profile = User.objects.get(username=username).profile
        is_follow = False
        is_user = False
        if v_user == profile:
            is_user = True 

        if profile_user_id.following.filter(id=v_user2).exists():
            is_follow = True
    '''

    context = {
        'follower_list': follower_list,
        'username': username,
    }

    return render(request, 'blog/follower.html', context)


def view_following(request, username):
    profile_user_id = get_object_or_404(User, username=username).profile
    follower_list = profile_user_id.follower.all()
    '''
    profile_user_id2 = get_object_or_404(User, username=username).profile.id
    v_user = User.objects.get(id=request.user.id).profile
    v_user2 = User.objects.get(id=request.user.id).profile.id
    profile = User.objects.get(username=username).profile
    is_follow = False
    is_user = False
    if v_user == profile:
        is_user = True 

    if profile_user_id.follower.filter(id=v_user2).exists():
        is_follow = True
    '''
    context = {
        'follower_list': follower_list,
        'username': username,
    }

    return render(request, 'blog/following.html', context)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'restrict_comment']
    template_name = 'blog/postupdate.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'restrict_comment']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CreatePostView(LoginRequiredMixin, View):
    model = Post
    fields = ['title', 'content', 'restrict_comment']
    template_name = 'post_form.html'

    def get(self, request):
        form = PostCreateForm()
        ImageFormset = modelformset_factory(Images, fields=('image',), extra=4)
        formset = ImageFormset(queryset=Images.objects.none())
        context = {
            'form': form,
            'formset': formset,
        }
        return render(request, 'blog/post_form.html', context)

    def post(self, request):
        ImageFormset = modelformset_factory(Images, fields=('image',), extra=4)
        if request.method == 'POST':
            form = PostCreateForm(request.POST, request.FILES or None)
            formset = ImageFormset(request.POST or None, request.FILES or None)
            # vidform = VideoForm(request.POST or None, request.FILES or None)
            if form.is_valid() and formset.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                words = form.cleaned_data['content']
                post.save()
                for word in words.split():
                    if word.startswith("#"):
                        if len(word) > 1:
                            hash_tag = HashTag(post=post, tag=word,user=request.user)
                            hash_tag.save()
                for word in words.split():
                    if word.startswith("@"):
                        w = word.replace('@', '')
                        try:
                            if User.objects.get(username__iexact=w):
                                if request.user != User.objects.get(username__iexact=w):
                                    notify.send(request.user, recipient=User.objects.get(username__iexact=w),
                                            verb='mentioned you in a post', action_object=post, description=words)
                        except User.DoesNotExist:
                            pass

                for f in formset:
                    try:
                        photo = Images(post=post, image=f.cleaned_data['image'])
                        photo.save()
                    except Exception as e:
                        break
                return redirect('blog-home')
        else:
            form = PostCreateForm()
            formset = ImageFormset(queryset=Images.objects.none())
            # vidform = VideoForm(queryset=Images.objects.none())

        context = {
            'form': form,
            'formset': formset, 
        }
        return render(request, 'blog/post_form.html', context)


def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    ImageFormset = modelformset_factory(Images, fields=('image',), extra=4, max_num=4)
    if request.method == 'POST':
        form = PostEditForm(request.POST or None, request.FILES or None, instance=post)
        formset = ImageFormset(request.POST or None, request.FILES or None) 
        if form.is_valid() and formset.is_valid():
            form.save() 
            data = Images.objects.filter(post=post)
            for index, f in enumerate(formset):
                if f.cleaned_data:
                    if f.cleaned_data['id'] is None:
                        photo = Images(post=post, image=f.cleaned_data.get('image'))
                        photo.save()

                    elif f.cleaned_data['image'] is False:
                        photo = Images.objects.get(id=request.POST.get('form-' + str(index) + "-id"))
                        photo.delete()
                    else:
                        photo = Images(post=post, image=f.cleaned_data.get('image'))
                        d = Images.objects.get(id=data[index].id)
                        d.image = photo.image
                        d.save()
            return HttpResponseRedirect(
                post.get_absolute_url())  # HttpResponseRedirect(reverse('post-detail', kwargs={'pk': pk}))  # HttpResponseRedirect(post.get_absolute_url())
    else:
        form = PostEditForm(instance=post)
        formset = ImageFormset(queryset=Images.objects.filter(post=post))

    context = {
        'form': form,
        'post': post,
        'formset': formset,
    }
    return render(request, 'blog/postupdate.html', context)
    # return HttpResponseRedirect(post.get_absolute_url())
    # return reverse('post-detail', kwargs={'pk': pk})


class EditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'restrict_comment']
    template_name = 'blog/postupdate.html'

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        post = get_object_or_404(Post, pk=pk)
        form = PostEditForm(instance=post)
        ImageFormset = modelformset_factory(Images, fields=('image',), extra=4, max_num=4)
        formset = ImageFormset(queryset=Images.objects.filter(post=post))

        context = {
            'form': form,
            'post': post,
        }
        return render(request, 'blog/postupdate.html', context)

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        prev_mentions = []
        prev_hashtags = []
        new_mentions = []
        new_hashtags = []
        post = get_object_or_404(Post, pk=pk)
        prev_post = PostEditForm(instance=post)
        prev_content = prev_post['content'].value() 
        for word in prev_content.split():
            if word.startswith("@"):
                prev_mentions.append(word)
        for word in prev_content.split():
            if word.startswith("#"):
                prev_hashtags.append(word)
        ImageFormset = modelformset_factory(Images, fields=('image',), extra=4, max_num=4)
        if request.method == 'POST':
            form = PostEditForm(request.POST or None, request.FILES or None, instance=post)
            formset = ImageFormset(request.POST or None, request.FILES or None)
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
                if len(diff_mentions) >= 1:
                    for word in diff_mentions:
                        if word.startswith("@"):
                            w = word.replace('@', '')
                            try:
                                if User.objects.get(username__iexact=w):
                                    if request.user != User.objects.get(username__iexact=w):
                                        notify.send(request.user, recipient=User.objects.get(username__iexact=w), verb='mentioned you in a post', action_object=post, description=content)
                            except User.DoesNotExist:
                                pass
                if len(diff_hastags) >= 1:
                    del_hash = HashTag.objects.filter(post__exact=pk)
                    del_hash.delete()
                    for word in new_hashtags:
                        if word.startswith("#"):
                            w = word.replace('#', '')
                            hash_tag = HashTag(post=post, tag=word,user=request.user)
                            hash_tag.save()
                data = Images.objects.filter(post=post)
                return HttpResponseRedirect(reverse('post-detail', kwargs={'pk': pk}))  # HttpResponseRedirect(post.get_absolute_url())
        else:
            form = PostEditForm(instance=post)
            formset = ImageFormset(queryset=Images.objects.filter(post=post))

        context = {
            'form': form,
            'post': post,
        }
        return HttpResponseRedirect(post.get_absolute_url())

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user or self.request.user.is_staff:
            return True
        return False

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PostReport(LoginRequiredMixin, CreateView):
    model = Report
    fields = ['content']

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        form = ReportForm()
        post = get_object_or_404(Post, pk=pk)
        context = {
            'form': form,
            'post': post
        }
        return render(request, 'blog/report_post.html', context)
    
    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        post = get_object_or_404(Post, pk=pk)
        if request.method == 'POST':
            report_form = ReportForm(request.POST or None)
            if report_form.is_valid():
                content = report_form.cleaned_data['content']
                report_create = Report.objects.create(user=request.user, post=post,content=content)
                report_create.save()
            messages.success(request, f'Report Submitted')
            return redirect('post-detail', pk=pk)
        else:
            form = ReportForm()
        context = {
            'form': form,
            'post': post
        }
        return render(request, 'blog/report_post.html', context)

class ShareReport(LoginRequiredMixin, CreateView):
    model = Report
    fields = ['content']

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        form = ReportForm()
        post = get_object_or_404(Share, pk=pk)
        context = {
            'form': form,
            'post': post
        }
        return render(request, 'blog/report_post.html', context)
    
    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        post = get_object_or_404(Share, pk=pk)
        if request.method == 'POST':
            report_form = ReportForm(request.POST or None)
            if report_form.is_valid():
                content = report_form.cleaned_data['content']
                report_create = Report.objects.create(user=request.user, shared_post=post,content=content)
                report_create.save()
            messages.success(request, f'Report Submitted') 
            return redirect('share-thread', pk=post.post.pk)
        else:
            form = ReportForm()
        context = {
            'form': form,
            'post': post
        }
        return render(request, 'blog/report_post.html', context)

class QuoteShare(LoginRequiredMixin, CreateView):
    model = Quote
    fields = ['content', 'share', 'user']
    context_object_name = 'share'

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        form = QuoteForm()
        share_post = get_object_or_404(Share, pk=pk)
        context = {
            'form': form,
            'share_post': share_post, 
        }
        return render(request, 'blog/quote.html', context)
    
    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        share_post = get_object_or_404(Share, pk=pk)
        if request.method == 'POST':
            quote_form = QuoteForm(request.POST or None, request.FILES or None)
            if quote_form.is_valid():
                image = quote_form.cleaned_data['image']
                content = quote_form.cleaned_data['content']
                share_pk = pk
                quote_create = Share.objects.create(post=share_post.post, share_post=share_post, is_quote=True, user=request.user, content = content, image=image)
                quote_create.save()
                for word in content.split():
                    if len(word) > 1:
                        if word.startswith("#"):
                            wo = word.replace('#', '')
                            hash_tag = ShareTag(share=quote_create, tag=wo, user=request.user)
                            hash_tag.save()
                for word in content.split():
                    if word.startswith("@"):
                        w = word.replace('@', '')
                        if User.objects.get(username__iexact=w):
                            notify.send(request.user, recipient=User.objects.get(username__iexact=w),
                                        verb='mentioned you in a post thread', action_object=share_post.post, description=content)
                        else:
                            pass
            messages.success(request, f'Done')
            return redirect('share-thread', pk=share_post.post.pk)
        else:
            form = QuoteForm()
        context = {
            'form': form,
            'share_post': share_post
        }
        return render(request, 'blog/quote.html', context)

class ShareView(LoginRequiredMixin, CreateView):
    model = Share
    fields = ['content', 'post', 'user']
    template_name = 'blog/share.html'
    success_url = '/'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        form = ShareForm()
        post = get_object_or_404(Post, pk=pk)
        context = {
            'form': form,
            'post': post,
        }
        return render(request, 'blog/share.html', context)

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        post = get_object_or_404(Post, pk=pk)
        if request.method == 'POST':
            share_form = ShareForm(request.POST or None, request.FILES or None)
            if share_form.is_valid():
                image = share_form.cleaned_data['image']  # request.POST.get('image')
                content = share_form.cleaned_data['content']
                post_id = pk
                share_create = Share.objects.create(post=post, user=request.user, content=content, image=image)
                share_create.save()
                for word in content.split():
                    if len(word) > 1:
                        if word.startswith("#"):
                            wo = word.replace('#', '')
                            hash_tag = ShareTag(share=share_create, tag=wo, user=request.user)
                            hash_tag.save()
                for word in content.split():
                    if word.startswith("@"):
                        w = word.replace('@', '')
                        if User.objects.get(username__iexact=w): 
                            notify.send(request.user, recipient=User.objects.get(username__iexact=w),
                                        verb='mentioned you in a post thread', action_object=post, description=content)
                        else:
                            pass
            messages.success(request, f'Post Shared')
            return redirect('share-thread', pk=pk)
        else:
            form = ShareForm()
        context = {
            'post': post,
            'form': form,
        }

        return render(request, 'blog/share.html', context)   


class ShareThread(ListView):
    model = Share
    paginate_by = 30
    context_object_name = 'shares'
    template_name = 'blog/post_thread.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['post_id'] = self.request.GET.get('pk')
        context['ori_post'] = Post.objects.get(pk=self.kwargs.get('pk'))
        return context

    def get_queryset(self):
        post_id = self.kwargs.get('pk')
        shares = Share.objects.filter(post__exact=post_id)
        share = shares.order_by('date_posted')
        return share

    # def get(self, request, *args, **kwargs):
    #     post_id = kwargs['pk']
    #     is_liked = False
    #     user = request.user.id
    #     shares = Share.objects.filter(post=post_id)
    #     for post in shares:
    #         if post.likes.filter(id=request.user.id).exists():
    #             is_liked = True
    #     share = shares.order_by('date_posted')
    #     ori_post = Post.objects.get(pk=post_id)
    #     context = {
    #         'shares': shares,
    #         'ori_post': ori_post,
    #         'is_liked': is_liked,
    #         'user_id':user
    #     }
    #     return render(request, 'blog/post_thread.html', context)

class ShareDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView, RedirectView):
    model = Share

    def test_func(self):
        share = self.get_object()
        if self.request.user == share.user:
            return True
        return False

    def get_success_url(self):
        return reverse('share-thread', kwargs={'pk': self.object.post.id})

class ShareEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView, RedirectView):
    model = Share
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
        share = Share.objects.get(pk=pk)
        form = ShareEditForm(instance=share)
        context = {
            'form': form,
            'post': share,
        }
        return render(request, 'blog/share_update.html', context)

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        share = Share.objects.get(pk=pk)
        form = ShareEditForm(instance=share)
        prev_mentions = []
        prev_hashtags = []
        new_mentions = []
        new_hashtags = []
        prev_post = ShareEditForm(instance=share)
        prev_content = prev_post['content'].value()
        for word in prev_content.split():
            if word.startswith("@"):
                prev_mentions.append(word)
        for word in prev_content.split():
            if word.startswith("#"):
                prev_hashtags.append(word)
        if request.method == 'POST':
            form = ShareEditForm(request.POST or None, request.FILES or None, instance=share) 
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
                if len(diff_mentions) >= 1:
                    for word in diff_mentions:
                        if word.startswith("@"):
                            w = word.replace('@', '')
                            try:
                                if User.objects.get(username__iexact=w):
                                    if request.user != User.objects.get(username__iexact=w):
                                        notify.send(request.user, recipient=User.objects.get(username__iexact=w), verb='mentioned you in a post thread', action_object=share.post, description=content)
                            except User.DoesNotExist:
                                pass
                if len(diff_hastags) >= 1:
                    del_hash = ShareTag.objects.filter(share__exact=pk)
                    del_hash.delete()                    
                    for word in new_hashtags:
                        if word.startswith("#"):
                            wo = word.replace('#', '')
                            hash_tag = ShareTag(share=share, tag=wo, user= request.user)
                            hash_tag.save()
                return HttpResponseRedirect(reverse('share-thread', kwargs={'pk': share.post.id}))
        else:
            form = ShareEditForm(instance=share)

        context = {
            'form': form,
            'share': share,
        }
        return HttpResponseRedirect(share.get_absolute_url())

    def get_success_url(self):
        return reverse('share-thread', kwargs={'pk': self.object.post.id})


def share_post(request, pk):
    post = get_object_or_404(Post, pk=pk) 

    '''if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            comment = Comment.objects.create(post=post, user=request.user, content=content, reply=comment_qs)
            comment.save()'''

    if request.method == 'POST':
        share_form = ShareForm(request.POST or None)
        if share_form.is_valid():
            content = request.POST.get('content')
            post_id = pk
            share_create = Share.objects.create(post=post, user=request.user, content=content)
            share_create.save()
        messages.success(request, f'Post Shared')
        return redirect('share-thread', pk=pk)
    else:
        form = ShareForm()
    context = {
        'post': post,
        'form': form,
    }

    return render(request, 'blog/share.html', context)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = self.object.user
        hit = self.object.hit_count.hits
        pro = Profile.objects.get(user=user)
        pro.deleted_post_views += hit
        pro.save()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


def trending(request):
    post = Post.objects.filter(hit_count_generic__gt=105)
    context ={
        'post':post
    }
    return render(request, 'blog/treding.html', context)

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
