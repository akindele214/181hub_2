from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpRequest, Http404, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods,require_safe
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, MonetizeForm
from .models import Profile, Monetization
from django.contrib.auth.models import User
from blog.models import Post
from django.contrib.auth.decorators import user_passes_test
from django.forms import modelformset_factory

from .models import AdminImages
from .forms import AdminUp
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            messages.success(request, f'Your Account Has Been Created You Are Now Able To Log In!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})


@login_required
def profile(request):
    views = 0
    total_post = Post.objects.filter(user=request.user)
    for post in total_post:
        views = views + post.hit_count.hits

    post_count = Post.objects.filter(user=request.user).count()

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Account Has Been Updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'total_views': views,
        'post_count': post_count,
        'user_update_form': u_form,
        'profile_update_form': p_form
    }
    return render(request, 'user/profile.html', context)

@require_safe
def monetize(request):
    if request.user.profile.verified:
        views = 0
        monetized_view = Profile.objects.get(user=request.user).monetized_views
        deleted_views = Profile.objects.get(user=request.user).deleted_post_views
        total_post = Post.objects.filter(user=request.user)
        is_cashable = False

        for post in total_post:
            views = views + post.hit_count.hits
        total_view = views + deleted_views
        if monetized_view is None:
            view_diff = total_view
        else:
            view_diff = total_view - monetized_view
        if view_diff > 500:
            is_cashable = True
        convert_to_money = round(view_diff * 0.6, 2)

        if request.method == 'POST':
            if request.user.profile.account_monetized == 0:
                mon_form = MonetizeForm(request.POST)
                if mon_form.is_valid():
                    # user = User.objects.get(id=request.user)
                    bank = request.POST.get('bank')
                    account_num = request.POST.get('account_num')
                    account_name = request.POST.get('account_name')
                    mon_final = Monetization.objects.create(user=request.user, views=view_diff, amount=convert_to_money, bank=bank, account_name=account_name, account_num=account_num)
                    mon_final.save()
                    e = Profile.objects.get(user=request.user)
                    e.account_monetized = True
                    e.monetized_views += total_view
                    e.save()
                    messages.success(request, f'Your Account Has Been Monetized And Cash-Out Request Submitted!')
                    return redirect('wallet')
            else:
                mon_form = MonetizeForm(request.POST)
                if mon_form.is_valid():
                    bank = request.POST.get('bank')
                    account_num = request.POST.get('account_num')
                    account_name = request.POST.get('account_name')
                    mon_final = Monetization.objects.create(user=request.user, views=view_diff, amount=convert_to_money, bank=bank, account_name=account_name, account_num=account_num)
                    mon_final.save()
                    pro = Profile.objects.get(user=request.user)
                    view_diff = total_view - monetized_view
                    if total_view > view_diff:
                        pro.monetized_views += view_diff
                        
                        pro.save()
                        messages.success(request, f'Your Cash-Out Request Submitted!')
                    return redirect('wallet')
        else:
            mon_form = MonetizeForm()

        context = {
            'form': mon_form,
            'money': convert_to_money,
            'views': views,
            'monetized_views': monetized_view,
            'is_cash': is_cashable
        }
        return render(request, 'user/monetize.html', context)
    else:
        raise Http404


@login_required
def wallet(request): 
    if request.user.profile.verified:
        views = 0
        monetized_view = Profile.objects.get(user=request.user).monetized_views
        deleted_views = Profile.objects.get(user=request.user).deleted_post_views
        total_post = Post.objects.filter(user__exact=request.user)
        orders = Monetization.objects.filter(user=request.user)
        is_cashable = False
        for post in total_post:
            views = views + post.hit_count.hits
        total_view = views + deleted_views
        print(total_view)
        if monetized_view == 0:
            view_diff = total_view
        else:
            view_diff = total_view - monetized_view

        if view_diff > 500:
            is_cashable = True
        post_count = Post.objects.filter(user=request.user).count()
        convert_to_money = round(view_diff * 0.6, 2)

        context = {
            'total_views': total_view,
            'post_count': post_count,
            'money': convert_to_money,
            'monetized_views': monetized_view,
            'is_cash': is_cashable,
            'orders': orders.order_by('-id'),
        }
        return render(request, 'user/wallet.html', context)

    else:
        raise Http404


def live_counter(request):
    if request.user.is_superuser: 
        count = User.objects.all().count()
        context = {
            'count': count,
        }
        return render(request, 'user/live_counter.html', context)
    else:
        raise Http404

class Admin(LoginRequiredMixin, UserPassesTestMixin,View):
    model = AdminUp

    def get(self, request):
        form = AdminUp()
        ImageFormset = modelformset_factory(AdminImages, fields=('image',), extra=4)
        formset = ImageFormset(queryset=AdminImages.objects.none())
        context = {
            'form': form,
            'formset': formset,
        }
        return render(request, 'blog/post_form.html', context)

    def post(self, request):
        ImageFormset = modelformset_factory(AdminImages, fields=('image',), extra=4)
        if request.method == 'POST':
            form = AdminUp(request.POST, request.FILES or None)
            formset = ImageFormset(request.POST or None, request.FILES or None)
            if form.is_valid() and formset.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                for f in formset:
                    try:
                        photo = AdminImages(admin=post, image=f.cleaned_data['image'])
                        photo.save()
                    except Exception as e:
                        break
                return redirect('blog-home')
        else:
            form = AdminUp()
            formset = ImageFormset(queryset=Images.objects.none())

        context = {
            'form': form,
            'formset': formset, 
        }
        return render(request, 'blog/post_form.html', context)

    def test_func(self):
        return self.request.user.is_superuser
