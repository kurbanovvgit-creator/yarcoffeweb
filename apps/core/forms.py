from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "field-input", "placeholder": "Ваше имя"}),
            "email": forms.EmailInput(attrs={"class": "field-input", "placeholder": "E-mail"}),
            "phone": forms.TextInput(attrs={"class": "field-input", "placeholder": "Телефон"}),
            "message": forms.Textarea(
                attrs={"class": "field-input field-textarea", "rows": 5, "placeholder": "Сообщение"}
            ),
        }
