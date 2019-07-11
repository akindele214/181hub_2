from django.shortcuts import render, get_object_or_404, redirect,reverse
from django.views.generic import ListView, View, CreateView, UpdateView, DeleteView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotFound, Http404
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from .models import Chat, ReportChat
from .forms import ReportForm
import json


def index(request):
    return render(request, 'chat/index.html', {})

@login_required
def dm(request, room_name):
    chat = Chat.objects.get(chat_id=room_name)
    if request.user in chat.participants.all() and request.user not in chat.deleted.all():
        if request.user_agent.is_mobile or request.user_agent.is_tablet:
            participants = None
            current_user = request.user
            current_chat = Chat.objects.get(chat_id=room_name)
            for participant in current_chat.participants.all():
                if participant != current_user:
                    participants=participant
            print(current_user)
            return render(request, 'chat/room.html', {
                'room_name_json': mark_safe(json.dumps(room_name)),
                'username': mark_safe(json.dumps(request.user.username)),
                'participants': participants,
                'current_user': current_user,
            })
        elif request.user_agent.is_pc:
            participants = None
            current_user = request.user
            current_chat = Chat.objects.get(chat_id=room_name)
            for participant in current_chat.participants.all():
                if participant != current_user:
                    participants=participant
            print(current_user)
            return render(request, 'chat/room_pc.html', {
                'room_name_json': mark_safe(json.dumps(room_name)),
                'username': mark_safe(json.dumps(request.user.username)),
                'participants': participants,
                'current_user': current_user,
            })
    else:
        # return HttpResponseNotFound()
        raise Http404('Chat Not Found')


@login_required
def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username))
    })

@login_required
def get_current_chat(chatId):
    return get_object_or_404(Chat, chat_id=chatId)

@login_required
def load_chat(request, receivers_id):
    requesting_users_id = request.user.id
    request_user = request.user
    receivers_user = User.objects.get(id__exact=receivers_id) 
    if receivers_user.profile.follower.filter(id__exact=request.user.profile.id).exists():
         print(22)

    if requesting_users_id > receivers_id:
        chat_room_id = str(requesting_users_id) + str(10110101) + str(receivers_id)
    else:
        chat_room_id = str(receivers_id) + str(10110101) + str(requesting_users_id)
    try:
        Chat.objects.get(chat_id=chat_room_id)
        chat=Chat.objects.get(chat_id=chat_room_id)
        return HttpResponseRedirect(reverse('dm', kwargs={'room_name':chat_room_id}))
    except Chat.DoesNotExist:
        combined_users = []
        combined_users.append(request_user)
        combined_users.append(receivers_user) 
        if receivers_user.profile.follower.filter(id__exact=request.user.profile.id).exists():
            Chat.objects.create(chat_id=chat_room_id, initiator=request_user, receiver=receivers_user, accept=True)
            get_chat = Chat.objects.get(chat_id=chat_room_id)
            get_chat.participants.set(combined_users)
            get_chat.save() 
            print('Chat Created')
            return HttpResponseRedirect(reverse('dm', kwargs={'room_name':chat_room_id}))
        else:
            Chat.objects.create(chat_id=chat_room_id, initiator=request_user, receiver=receivers_user, accept=False)
            get_chat = Chat.objects.get(chat_id=chat_room_id)
            get_chat.participants.set(combined_users)
            get_chat.save()
            print('Chat Request Created')
            return HttpResponseRedirect(reverse('dm', kwargs={'room_name':chat_room_id}))

@login_required
def messages(request):
    if request.user_agent.is_mobile or request.user_agent.is_tablet:
        print('mobile')
        user_id = request.user.id 

        chat = Chat.objects.filter(participants__exact=user_id).exclude(receiver=request.user, accept=False).order_by('-date_updated')
        chat = chat.exclude(deleted=user_id)
        chat_request = Chat.objects.filter(participants__exact=user_id, accept=False).exclude(initiator=request.user).order_by('-date_updated')
        count = 0
        request_page = False
        
        print(chat)
        context = {
            'chat':chat,
            'chat_request': chat_request,
            'count': count,
            'request_page': request_page
        }
        return render(request, 'chat/messager.html', context)
    elif request.user_agent.is_pc:
        print('pc')
        user_id = request.user.id 
        chat = Chat.objects.filter(participants__exact=user_id).exclude(deleted__exact=user_id,receiver=request.user, accept=False).order_by('-date_updated')

        chat_request = Chat.objects.filter(participants__exact=user_id, accept=False).exclude(initiator=request.user).order_by('-date_updated')
        count = 0
        request_page = False
        context = {
            'chat':chat,
            'chat_request': chat_request,
            'count': count,
            'request_page': request_page
        }
        return render(request, 'chat/messager_pc.html', context)

@login_required
def unaccepted_messages(request):
    if request.user_agent.is_mobile or request.user_agent.is_tablet:
        print('mobile')
        user_id = request.user.id
        chat = Chat.objects.filter(participants__exact=user_id, accept=False).exclude(initiator=request.user).order_by('-date_updated')
        request_page = True
        count = 0
        context = {
            'chat':chat,
            'count': count,
            'request_page': request_page
        }
        return render(request, 'chat/messager.html', context)
    elif request.user_agent.is_pc:
        print('pc')
        user_id = request.user.id
        chat = Chat.objects.filter(participants__exact=user_id, accept=False).exclude(initiator=request.user).order_by('-date_updated')
        count = 0
        request_page = True
        context = {
            'chat':chat,
            'count': count,
            'request_page': request_page
        }
        return render(request, 'chat/messager_pc.html', context)

@login_required
def delete_chat(request, chat_id):
    chat = Chat.objects.get(chat_id=chat_id)
    if request.user in chat.participants.all():
        chat.deleted.add(request.user)
        chat.save()
        
        print('deleted')
        diff = list(set(chat.deleted.all()) - set(chat.participants.all()) )
        print(diff)
        print(chat.deleted.all())
        print(chat.participants.all())
        print( set(chat.deleted.all()) == set(chat.participants.all()) )
        if set(chat.deleted.all()) == set(chat.participants.all()):
            chat.messages.all().delete()
            chat.delete()
        else:
            print('no')
        return HttpResponseRedirect(reverse('messenger'))
    else:
        return HttpResponseForbidden()


class ChatReport(LoginRequiredMixin, CreateView):
    model = Chat
    fields = ['content']

    def get(self, request, *args, **kwargs):
        pk = kwargs['chat_id']
        form = ReportForm()
        chat = get_object_or_404(Chat, chat_id=pk)
        context = {
            'form': form,
            'chat': chat
        }
        return render(request, 'chat/report.html', context)
    
    def post(self, request, *args, **kwargs):
        pk = kwargs['chat_id']
        chat = get_object_or_404(Chat, chat_id=pk)
        if request.method == 'POST':
            report_form = ReportForm(request.POST or None)
            if report_form.is_valid():
                content = report_form.cleaned_data['content']
                report_create = ReportChat.objects.create(user=request.user, chat=chat,content=content)
                report_create.save() 
            return redirect('messenger')
        else:
            form = ReportForm()
        context = {
            'form': form,
            'post': post
        }
        return render(request, 'chat/report.html', context)