from django import forms

from .models import Customer

BASE_INPUT_CLASS = "input input-sm w-full"


class CustomerForm(forms.ModelForm):
    def clean_document_id(self):
        document_id = self.cleaned_data["document_id"]
        qs = Customer.objects.filter(document_id=document_id)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe un cliente con este DNI.")
        return document_id

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip().lower()
        if email:
            qs = Customer.objects.filter(email__iexact=email)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Ya existe un cliente con este correo.")
        return email

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
            "document_id": forms.TextInput(
                attrs={
                    "class": BASE_INPUT_CLASS,
                    "maxlength": "8",
                    "minlength": "8",
                    "pattern": r"\d{8}",
                    "inputmode": "numeric",
                    "placeholder": "8 digitos",
                }
            ),
            "email": forms.EmailInput(attrs={"class": BASE_INPUT_CLASS}),
            "phone": forms.TextInput(
                attrs={
                    "class": BASE_INPUT_CLASS,
                    "maxlength": "9",
                    "minlength": "9",
                    "pattern": r"\d{9}",
                    "inputmode": "numeric",
                    "placeholder": "9 digitos",
                }
            ),
            "is_active": forms.CheckboxInput(attrs={"class": "checkbox checkbox-sm checkbox-primary"}),
        }
