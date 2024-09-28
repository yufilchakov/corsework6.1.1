from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render

from blog.models import Blog
from mailing.forms import ClientForm, MessageForm, MailingForm, ManagerMailingForm
from mailing.models import Client, Message, Mailing, Attempt
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.conf import settings
from django.core.exceptions import PermissionDenied


def index(request):
    mailing_count = Mailing.objects.count()
    active_mailing_count = Mailing.objects.filter(status='active').count()
    unique_clients_count = Mailing.objects.values('client').distinct().count()
    random_articles = Blog.objects.order_by('?')[:3]
    
    context = {
        'mailing_count': mailing_count,
        'active_mailing_count': active_mailing_count,
        'unique_clients_count': unique_clients_count,
        'random_articles': random_articles,
    }
    
    if mailing_count == 0 or random_articles.count() == 0:
        context['error_message'] = 'Нет данных для отображения.'
    
    return render(request, 'mailing/index.html', context)


class ClientListView(ListView):
    model = Client
    template_name = 'mailing/client_list.html'
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Список клиентов'
        return context_data


class ClientDetailView(DetailView):
    model = Client
    template_name = 'mailing/client_detail.html'
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Информация о клиенте'
        context_data['client'] = self.get_object()
        return context_data


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')
    template_name = 'mailing/client_form.html'
    
    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')
    template_name = 'mailing/client_form.html'
    
    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ClientForm
        if user.has_perm('client.man_view_the_list_of_service_users') and user.has_perm(
                'client.may_block_users_of_the_service'):
            return ManagerMailingForm
        raise PermissionDenied


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')
    template_name = 'mailing/client_confirm_delete.html'


class MessageListView(ListView):
    model = Message
    template_name = 'mailing/message_list.html'
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Список писем'
        return context_data


class MessageDetailView(DetailView):
    model = Message
    template_name = 'mailing/message_detail.html'
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Информация о письме'
        return context_data


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')
    template_name = 'mailing/message_form.html'
    
    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')
    template_name = 'mailing/message_form.html'
    
    def form_valid(self, form):
        message_id = form.cleaned_data['message']
        if Mailing.objects.filter(message=message_id).exists():
            pass
        else:
            return super().form_valid(form)
        
    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MessageForm
        if user.has_perm('message.can_view_messages') and user.has_perm(
                'message.can_edit_messages'):
            return ManagerMailingForm
        raise PermissionDenied


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')
    template_name = 'mailing/message_confirm_delete.html'


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Список рассылок'
        return context_data


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Информация о рассылки'
        return context_data


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')
    template_name = 'mailing/mailing_form.html'
    
    def form_valid(self, form):
        message = form.cleaned_data['message']
        subject_of_the_letter = message.subject_of_the_letter
        body_of_the_letter = message.body_of_the_letter
        email_from = settings.EMAIL_HOST_USER
        client = form.cleaned_data['client'].first()
        email = [client.email, ]
        
        try:
            send_mail(subject_of_the_letter, body_of_the_letter, email_from, email)
        except BadHeaderError:
            return HttpResponse('Ошибка отправки.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_invalid(form)
       

class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')
    template_name = 'mailing/mailing_form.html'
    
    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MailingForm
        if user.has_perm('mailing.can_view_any_mailings') and user.has_perm(
                'mailing.can_disable_mailings'):
            return ManagerMailingForm
        raise PermissionDenied


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')
    template_name = 'mailing/mailing_confirm_delete.html'


class AttemptListView(ListView):
    model = Attempt
    template_name = 'mailing/attempt_list.html'
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Список попыток'
        return context_data


class AttemptDetailView(DetailView):
    model = Attempt
    template_name = 'mailing/attempt_detail.html'
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Информация о попытки рассылки'
        return context_data
