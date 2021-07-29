import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

import local_settings
from crm import telegram_bot
from .filters import UserFilter
from .models import User, Contact
from .forms import UserRegistrationForm, UserDetailForm, UserContactsForm


class UserListView(LoginRequiredMixin, generic.ListView):

    model = User
    paginate_by = 25

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponse('<h1>403 Forbidden</h1>', status=403,)
        else:
            return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        filter = UserFilter(self.request.GET, queryset=User.objects.all())
        context['filter'] = filter
        return context


class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = User

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_staff and self.request.user.id != int(self.kwargs['pk']):
            return HttpResponse('<h1>403 Forbidden</h1>', status=403,)
        else:
            return super().get(self, request, *args, **kwargs)


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})


@login_required
def user_detail_update(request, pk):

    if not request.user.is_staff and request.user.id != int(pk):
        return HttpResponse('<h1>403 Forbidden</h1>', status=403, )

    lookup_user = User.objects.get(id=pk)
    try:
        contacts = Contact.objects.get(user_id=pk)
    except ObjectDoesNotExist:
        contacts = Contact.objects.create(user=lookup_user)

    if request.method == 'POST':
        user_form = UserDetailForm(request.POST, instance=lookup_user)
        contacts_form = UserContactsForm(request.POST, instance=contacts)

        if user_form.is_valid() and contacts_form.is_valid():
            new_data = user_form.save(commit=False)
            new_data.save()
            user_contacts = contacts_form.save()
            user_contacts.save()
            return HttpResponseRedirect(reverse('user-detail', kwargs={'pk': pk}))

    else:
        user_form = UserDetailForm(instance=lookup_user)
        contacts_form = UserContactsForm(instance=contacts)

    context = {'user_form': user_form, 'contacts_form': contacts_form, 'pk': pk}
    return render(request, 'user_detail_update.html', context)


@login_required
def subscribe_to_updates(request):

    chat_bot_name = os.environ.get('DJANGO_TELEGRAM_BOT_NAME', local_settings.TELEGRAM_BOT_NAME)

    if request.user.is_sub:
        return HttpResponseRedirect(reverse('user-detail', kwargs={'pk': request.user.id}))

    if request.method == 'POST':
        contact = Contact.objects.get(user=request.user.id)
        telegram_bot.get_update()
        username = contact.telegram
        chat_id = telegram_bot.get_chat_id(username)
        if chat_id:
            request.user.is_sub = True
            request.user.save(update_fields=['is_sub'])
            contact.chat_bot_id = chat_id
            contact.save(update_fields=['chat_bot_id'])
            return HttpResponseRedirect(reverse('user-detail', kwargs={'pk': request.user.id}))
        return render(request, 'sub_confirm.html', {'chat_bot_name': chat_bot_name})
    else:
        return render(request, 'sub_confirm.html', {'chat_bot_name': chat_bot_name})
