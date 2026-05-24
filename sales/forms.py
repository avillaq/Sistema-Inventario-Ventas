from django import forms

from .models import Customer

BASE_INPUT_CLASS = "input input-sm w-full"


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            "full_name",
            "document_id",
            "email",
            "phone",
            "is_active",
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": BASE_INPUT_CLASS}),
            "document_id": forms.TextInput(attrs={"class": BASE_INPUT_CLASS}),
            "email": forms.EmailInput(attrs={"class": BASE_INPUT_CLASS}),
            "phone": forms.TextInput(attrs={"class": BASE_INPUT_CLASS}),
            "is_active": forms.CheckboxInput(attrs={"class": "checkbox checkbox-sm checkbox-primary"}),
        }
