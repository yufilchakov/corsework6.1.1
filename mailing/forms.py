from django.forms import ModelForm, forms, BooleanField, ModelMultipleChoiceField
from mailing.models import Client, Message, Mailing
from django.forms.widgets import DateTimeInput, SelectMultiple


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs['class'] = 'form-check-input'
            else:
                fild.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Client
        fields = '__all__'


class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
       

class MailingForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Mailing
        fields = '__all__'
        widgets = {
            'start_date': DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': DateTimeInput(attrs={'type': 'datetime-local'}),
            'next_send_time': DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        message = ModelMultipleChoiceField(queryset=Message.objects.all(),
                                           widget=SelectMultiple(attrs={'class': 'form-control'}))
        client = ModelMultipleChoiceField(queryset=Client.objects.all(),
                                          widget=SelectMultiple(attrs={'class': 'form-control'}))
        
        def clean_client(self):
            client = self.cleaned_data['client']
            if not client:
                raise forms.ValidationError('Требуется клиент')
            return client


class MailingManagerForm(StyleFormMixin, ModelForm):
    """Класс форма для менеджера изменение рассылок."""
    
    class Meta:
        model = Mailing
        fields = ('client', 'message', 'periodicity', 'start_date', 'end_date')


class MailingModeratorForm(StyleFormMixin, ModelForm):
    """Класс форма для модератора изменение рассылок."""
    
    class Meta:
        model = Mailing
        fields = ('client', 'message', 'periodicity', 'start_date', 'end_date')
