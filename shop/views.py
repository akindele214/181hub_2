from .models import Product, ProductImage
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, View, CreateView, UpdateView, DeleteView, RedirectView, DetailView
from django.http import JsonResponse, HttpResponseRedirect, Http404  # HttpResponse, Http404
from .forms import ProductCreateForm
from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404, redirect, reverse
from hitcount.views import HitCountDetailView
from hitcount.models import HitCount
from django.views.decorators.csrf import ensure_csrf_cookie
from itertools import chain
from django.db.models import Q


# REST FRAMEWORK
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User


# Create your views here.

class AdList(ListView):
    model = Product
    template_name = 'shop/home.html'
    ordering = ['-date_posted']
    context_object_name = 'posts'
    paginate_by = 30

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['model'] = self.model
        return context

    def get_queryset(self):
        posts = Product.objects.all().order_by('-date_posted')
        # print(ads)
        return posts

class CategoryList(ListView):
    model = Product
    template_name = 'shop/category.html'
    ordering = ['-date_posted']
    context_object_name = 'posts'
    paginate_by = 30

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['model'] = self.model
        context['category'] = self.kwargs['category']
        print(context)
        return context

    def get_queryset(self):
        category = self.kwargs['category']
        posts = Product.objects.filter(
                Q(prod_category__icontains=category)).order_by('-date_posted')
        # print(ads)
        return posts


class CreateProductView(LoginRequiredMixin, CreateView):
    model = Product

    def get(self, request):
        form = ProductCreateForm()
        ImageFormset = modelformset_factory(ProductImage, fields=('image',), extra=4)
        formset = ImageFormset(queryset=ProductImage.objects.none())

        context = {
            'form': form,
            'formset': formset,
        }
        return render(request, 'shop/post_form.html', context)

    def post(self, request):
        ImageFormset = modelformset_factory(ProductImage, fields=['image'], extra=4)
        
        if request.method == 'POST':
            form = ProductCreateForm(request.POST, request.FILES or None)
            formset = ImageFormset(request.POST or None, request.FILES or None)

            if form.is_valid() and formset.is_valid():
                prod = form.save(commit=False)
                prod.user = request.user
                prod.save()
                
                for f in formset:
                    try:
                        prod_image = ProductImage(prod=prod, image=f.cleaned_data['image'])
                        prod_image.save()
                    except Exception as e:
                        pass
                return redirect('blog-home')
        
        else:
            form = ProductCreateForm()
            formset = ImageFormset(queryset=Images.objects.none())
        
        context = {
            'form' :form,
            'formset': formset,
        }
        return render(request, 'shop/post_form.html', context)

class ProductMixinDetailView(object):
    """
    Mixin to same us some typing.  Adds context for us!
    """
    model = Product

    def get_context_data(self, **kwargs):
        context = super(PostMixinDetailView, self).get_context_data(**kwargs)
        context['post_list'] = Product.objects.all()[:]
        context['post_views'] = ["ajax", "detail", "detail-with-count"]
        return context

class ViewProductDetail(DetailView):
    model = Product
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(ViewProductDetail, cls).as_view(**initkwargs)
        return ensure_csrf_cookie(view)
    
    def get(self, request,*args, **kwargs):
        pk = kwargs['pk']
        item = get_object_or_404(Product, pk=pk)
        userID = request.user.id

        is_cart = False
        is_saved = False

        # if userID in item.saved.all():
        #     is_saved = True
        if userID in item.saved.all():
            is_cart = True
        

        context = {
            'object': item,
            'is_saved': is_saved,
            'is_cart': is_cart
        }

        return render(request, 'shop/item_detail.html', context)

class ProductLikeToggle(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        print(pk)
        obj = get_object_or_404(Product, pk=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_

class ProductLikeAPIToggle(APIView):
    
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None, format=None):
        # pk = self.kwargs.get('pk')
        obj = get_object_or_404(Product, pk=pk)
        # url_ = obj.get_absolute_url()
        user = self.request.user
        updated = False
        is_liked = False

        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
                is_liked = False
            else:
                obj.likes.add(user)
                is_liked = True

                # if request.user != obj.user:
                #     notify.send(request.user, recipient=obj.user, verb='liked your post', action_object=obj)

            updated = True
        data = {
            "updated": updated,
            "is_liked": is_liked,
            "like_count": obj.likes.count(),
        }
        print(data)
        return Response(data)


class ProductSaveToggle(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        print(pk)
        obj = get_object_or_404(Product, pk=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.saved.all():
                obj.saved.remove(user)
            else:
                obj.saved.add(user)
        return url_


class ProductSaveAPIToggle(APIView):
    
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None, format=None):
        # pk = self.kwargs.get('pk')
        obj = get_object_or_404(Product, pk=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user
        updated = False
        saved = False

        if user.is_authenticated:
            if user in obj.saved.all():
                obj.saved.remove(user)
                saved = False
            else:
                obj.saved.add(user)
                saved = True

                # if request.user != obj.user:
                #     notify.send(request.user, recipient=obj.user, verb='liked your post', action_object=obj)

            updated = True
        data = {
            "updated": updated,
            "is_saved": saved,
        }
        return Response(data)

class SavedAdListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'shop/saved_ad.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 30

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['model'] = self.model
        context['page'] = 'Saved'
        return context
    
    def get_queryset(self):
        users = self.request.user 
        post_results = Product.objects.filter(saved__exact=users).order_by('-date_posted')
        queryset_chain = chain(post_results)
        qs = sorted(queryset_chain, key=lambda instance: instance.date_posted, reverse=True)
        return qs


class UserAdView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'shop/saved_ad.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 30

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['model'] = self.model
        context['page'] = 'My' 
        return context
    
    def get_queryset(self):
        users = self.request.user 
        post_results = Product.objects.filter(user__exact=users).order_by('-date_posted')
        queryset_chain = chain(post_results)
        qs = sorted(queryset_chain, key=lambda instance: instance.date_posted, reverse=True)
        return qs


class AdDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

    def get_success_url(self):
        return reverse('my-ads')    