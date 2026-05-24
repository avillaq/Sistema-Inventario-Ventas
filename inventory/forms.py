from django import forms

from .models import Brand, Category, Product

BASE_INPUT_CLASS = "rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-800"
BASE_SELECT_CLASS = "rounded-2xl border border-slate-200 bg-white px-3 py-3 text-sm text-slate-800"


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(is_active=True)
        self.fields["brand"].queryset = Brand.objects.filter(is_active=True)

    class Meta:
        model = Product
        fields = [
            "barcode",
            "name",
            "cost",
            "price",
            "stock",
            "min_stock",
            "category",
            "brand",
            "is_active",
        ]
        widgets = {
            "barcode": forms.TextInput(attrs={"class": BASE_INPUT_CLASS}),
            "name": forms.TextInput(attrs={"class": BASE_INPUT_CLASS}),
            "cost": forms.NumberInput(attrs={"class": BASE_INPUT_CLASS, "step": "0.01"}),
            "price": forms.NumberInput(attrs={"class": BASE_INPUT_CLASS, "step": "0.01"}),
            "stock": forms.NumberInput(
                attrs={"class": BASE_INPUT_CLASS, "min": "0", "max": Product.MAX_STOCK}
            ),
            "min_stock": forms.NumberInput(
                attrs={"class": BASE_INPUT_CLASS, "min": "0", "max": Product.MAX_STOCK}
            ),
            "category": forms.Select(attrs={"class": BASE_SELECT_CLASS}),
            "brand": forms.Select(attrs={"class": BASE_SELECT_CLASS}),
            "is_active": forms.CheckboxInput(attrs={"class": "checkbox checkbox-sm"}),
        }
