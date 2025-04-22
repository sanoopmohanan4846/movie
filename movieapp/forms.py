from django import forms
from django.core.validators import EmailValidator

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    subject = forms.CharField(max_length=100)
    email = forms.EmailField(validators=[EmailValidator()])
    phone = forms.CharField(max_length=10)
    description = forms.CharField(widget=forms.Textarea)
    