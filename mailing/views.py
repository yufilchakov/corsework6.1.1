from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render
from blog.models import Blog
from mailing.forms import ClientForm, MessageForm, MailingForm, MailingManagerForm
from mailing.models import Client, Message, Mailing, Attempt
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.conf import settings
from django.core.exceptions import PermissionDenied

from mailing.task import get_index_from_cache


def index(request):
    """ Обрабатывает запрос на главную страницу сайта. """
    mailing_count = Mailing.objects.count()
    launched_mailing_count = Mailing.objects.filter(status='active').count()
    unique_clients_count = Mailing.objects.values('client').distinct().count()
    random_articles = Blog.objects.order_by('?')[:3]
    
    context = {
        'mailing_count': mailing_count,
        'launched_mailing_count': launched_mailing_count,
        'unique_clients_count': unique_clients_count,
        'random_articles': random_articles,
    }
    
    if mailing_count == 0 or random_articles.count() == 0:
        context['error_message'] = 'Нет данных для отображения.'
    
    return render(request, 'mailing/index.html', context)
    
    
def get_queryset(self):
    return get_index_from_cache()()


class ClientListView(ListView):
    """ Является представлением списка клиентов. """
    model = Client
    template_name = 'mailing/client_list.html'
    
    def get_context_data(self, **kwargs):
        """ Метод формирует контекст для шаблона. """
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Список клиентов'
        return context_data
    
    def get_queryset(self):
        """ Возвращает содержащий только клиентов. """
        return Client.objects.filter(owner=self.request.user)


class ClientDetailView(DetailView):
    """ Является представлением детального просмотра клиента. """
    model = Client
    template_name = 'mailing/client_detail.html'
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Информация о клиенте'
        context_data['client'] = self.get_object()
        return context_data


class ClientCreateView(CreateView):
    """ Класс является представлением для создания нового клиента. """
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')
    template_name = 'mailing/client_form.html'
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    """Класс является представлением для обновления информации о клиенте. """
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')
    template_name = 'mailing/client_form.html'
    
    def get_form_class(self):
        """ Метод возвращает класс формы, используемый для обновления информации о клиенте. """
        user = self.request.user
        if user == self.object.owner:
            return ClientForm
        if user.has_perm('client.man_view_the_list_of_service_users') and user.has_perm(
                'client.may_block_users_of_the_service'):
            return MailingManagerForm
        raise PermissionDenied


class ClientDeleteView(DeleteView):
    """ Класс является представлением для удаления клиента. """
    model = Client
    success_url = reverse_lazy('mailing:client_list')
    template_name = 'mailing/client_confirm_delete.html'


class MessageListView(ListView):
    """ Класс является представлением списка писем. """
    model = Message
    template_name = 'mailing/message_list.html'
    
    def get_context_data(self, **kwargs):
        """ Метод формирует контекст для шаблона. """
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Список писем'
        return context_data
    
    def get_queryset(self):
        """ Возвращает содержащие только письма текущего пользователя. """
        return Message.objects.filter(owner=self.request.user)


class MessageDetailView(DetailView):
    """ Класс является представлением детального просмотра письма. """
    model = Message
    template_name = 'mailing/message_detail.html'
    
    def get_context_data(self, **kwargs):
        """ Метод формирует контекст для шаблона. """
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Информация о письме'
        return context_data


class MessageCreateView(CreateView):
    """ Класс является представлением для создания нового письма. """
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')
    template_name = 'mailing/message_form.html'
    
    def form_valid(self, form):
        """ Метод присваивает владельца создаваемому объекту. """
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(UpdateView):
    """ Класс является представлением для обновления информации о письме. """
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')
    template_name = 'mailing/message_form.html'
    
    def form_valid(self, form):
        """ Метод проверяет, что письмо не уже входит в рассылку. """
        message_id = form.cleaned_data['message']
        if Mailing.objects.filter(message=message_id).exists():
            pass
        else:
            return super().form_valid(form)
    
    def get_form_class(self):
        """ Метод возвращает класс формы, используемый для обновления информации о письме. """
        user = self.request.user
        if user == self.object.owner:
            return MessageForm
        if user.has_perm('message.can_view_messages') and user.has_perm(
                'message.can_edit_messages'):
            return MailingManagerForm
        raise PermissionDenied


class MessageDeleteView(DeleteView):
    """ Класс является представлением для удаления письма. """
    model = Message
    success_url = reverse_lazy('mailing:message_list')
    template_name = 'mailing/message_confirm_delete.html'


class MailingListView(ListView):
    """ Класс является представлением списка рассылок. """
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    
    def get_context_data(self, **kwargs):
        """ Метод формирует контекст для шаблона. """
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Список рассылок'
        return context_data
    
    def get_queryset(self):
        """ Возвращает содержащие только рассылки текущего пользователя. """
        return Mailing.objects.filter(owner=self.request.user)


class MailingDetailView(DetailView):
    """ Класс является представлением детального просмотра рассылки. """
    model = Mailing
    template_name = 'mailing/mailing_detail.html'
    
    def get_context_data(self, **kwargs):
        """ Метод формирует контекст для шаблона. """
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Информация о рассылки'
        return context_data


class MailingCreateView(CreateView):
    """ Класс является представлением для создания нового рассылки. """
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')
    template_name = 'mailing/mailing_form.html'
    
    def form_valid(self, form):
        """ Метод присваивает владельца создаваемому объекту. """
        form.instance.owner = self.request.user
        message = form.cleaned_data['message']
        subject_of_the_letter = message.subject_of_the_letter
        body_of_the_letter = message.body_of_the_letter
        email_from = settings.EMAIL_HOST_USER
        client = form.cleaned_data['client']
        email = [client.email, ]
        
        try:
            send_mail(subject_of_the_letter, body_of_the_letter, email_from, email)
        except BadHeaderError:
            return HttpResponse('Ошибка отправки.')
        return super().form_valid(form)


class MailingUpdateView(UpdateView):
    """ Класс является представлением для обновления информации о рассылке. """
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')
    template_name = 'mailing/mailing_form.html'
    
    def get_form_class(self):
        """ Метод возвращает класс формы, используемый для обновления информации о рассылке. """
        user = self.request.user
        if user == self.object.owner:
            return MailingForm
        if user.has_perm('mailing.can_view_any_mailings') and user.has_perm(
                'mailing.can_disable_mailings'):
            return MailingManagerForm
        raise PermissionDenied


class MailingDeleteView(DeleteView):
    """ Класс является представлением для удаления рассылки. """
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')
    template_name = 'mailing/mailing_confirm_delete.html'


class AttemptListView(ListView):
    """ Класс является представлением списка попыток рассылки. """
    model = Attempt
    template_name = 'mailing/attempt_list.html'
    
    def get_context_data(self, **kwargs):
        """ Метод формирует контекст для шаблона. """
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Список попыток'
        return context_data


class AttemptDetailView(DetailView):
    """ Класс является представлением для отображения детальной информации о попытке рассылки. """
    model = Attempt
    template_name = 'mailing/attempt_detail.html'
    
    def get_context_data(self, **kwargs):
        """ Метод возвращает контекст для шаблона отображения детальной информации о попытке рассылки. """
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Информация о попытки рассылки'
        return context_data
