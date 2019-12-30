from django import forms
from django.core.mail import EmailMessage
from .models import Pulse_Rate


class InquiryForm(forms.Form):
    name = forms.CharField(label='name', max_length=20)
    email = forms.EmailField(label='email')
    title = forms.CharField(label='title', max_length=20)
    message = forms.CharField(label='message', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'form-control col-9'
        self.fields['name'].widget.attrs['placeholder'] = 'your name'

        self.fields['email'].widget.attrs['class'] = 'form-control col-11'
        self.fields['email'].widget.attrs['placeholder'] = 'your email'

        self.fields['title'].widget.attrs['class'] = 'form-control col-11'
        self.fields['title'].widget.attrs['placeholder'] = 'write title'

        self.fields['message'].widget.attrs['class'] = 'form-control col-12'
        self.fields['message'].widget.attrs['placeholder'] = 'write message'

    def send_email(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        title = self.cleaned_data['title']
        message = self.cleaned_data['message']

        subject = 'Inquiry {}'.format(title)
        message = 'Sender Name: {0}\nEmail: {1}\nMessage:\n{2}'.format(name, email, message)
        from_email = 'admin@example.com'
        to_list = [
            'test@example.com'
        ]
        cc_list = [
            email
        ]

        message = EmailMessage(subject=subject, body=message, from_email=from_email, to=to_list, cc=cc_list)
        message.send()


class PulseRateCreateForm(forms.ModelForm):
    class Meta:
        model = Pulse_Rate
        fields = ('title', 'data',)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'


class PulseRateFilterForm(forms.ModelForm):
    class Meta:
        model = Pulse_Rate
        fields = ('fc_low', 'fc_high',)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.files.values():
                field.widget.attrs['class'] = 'form-control'
