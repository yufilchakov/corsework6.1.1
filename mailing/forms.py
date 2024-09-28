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
        fields = ['id', 'email', 'last_name', 'first_name', 'patronymic', 'comment']


class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        fields = ['subject_of_the_letter', 'body_of_the_letter']
       

class MailingForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Mailing
        fields = ['start_date', 'end_date', 'periodicity', 'status', 'message', 'client']
        widgets = {
            'start_date': DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': DateTimeInput(attrs={'type': 'datetime-local'}),
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


class ManagerMailingForm(StyleFormMixin, ModelForm):
    """Класс форма для менеджера изменение рассылок"""
    
    class Meta:
        model = Mailing
        fields = ('client', 'message', 'periodicity', 'start_date', 'end_date')
        